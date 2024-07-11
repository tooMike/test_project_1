from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.mixins import CreateModelViewSet, GetListViewSet
from api.permissions import IsOwner
from api.serializers import (
    CartCreateSerializer,
    CartDeleteSerializer,
    CartListSerializer,
    CartUpdateSerializer,
    CategorySerializer,
    ProductSerializer, UserRegistrationSerializer,
)
from shop.models import Category, Product, ShoppingCart

User = get_user_model()


class UserCreateViewSet(CreateModelViewSet):
    """Представление для регистрации пользователя."""

    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ('post',)


class CategoryViewSet(GetListViewSet):
    """Представление для категорий и подкатегорий."""

    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination


class ProductViewSet(GetListViewSet):
    """Представление для товаров."""

    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination


class CartViewSet(viewsets.ModelViewSet):
    """Представление для корзины."""

    permission_classes = (IsOwner,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = CartListSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return CartListSerializer
        elif self.action == 'create':
            return CartCreateSerializer
        elif self.action == 'partial_update':
            return CartUpdateSerializer
        else:
            return CartDeleteSerializer

    def list(self, request, *args, **kwargs):
        """Получение информации о всей корзине."""
        queryset = self.get_queryset()

        total_quantity = queryset.aggregate(total_quantity=Sum('quantity'))[
            'total_quantity']
        total_price = queryset.aggregate(
            total_price=Sum(F('quantity') * F('product__price'))
        )['total_price']

        data = {
            'products': queryset,
            'total_quantity': total_quantity,
            'total_price': total_price,
        }

        serializer = self.get_serializer_class()(data)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Добавление товара в корзину."""
        serializer = self.get_serializer_class()(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

    def partial_update(self, request, *args, **kwargs):
        """Изменения количества товара в корзине."""
        serializer = self.get_serializer_class()(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            cart = self.get_queryset().filter(
                product=serializer.validated_data["product"]
            ).first()
            if cart:
                cart.quantity = serializer.validated_data[
                    "quantity"]
                cart.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"errors": "Этого товара нет в корзине"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        request_body=CartDeleteSerializer,
        responses={204: 'No Content', 400: 'Bad Request'}
    )
    def destroy(self, request, *args, **kwargs):
        """Удаление товара из корзины."""
        serializer = self.get_serializer_class()(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            cart = self.get_queryset().filter(
                product=serializer.validated_data["product"]
            ).first()
            if cart:
                cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"errors": "Этого товара нет в корзине"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(methods=['delete'], detail=False)
    def clear(self, request):
        """Очистка всей корзины."""
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

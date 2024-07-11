from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from shop.models import Category, Product, ShoppingCart, SubCategory

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data["password"] = make_password(
            validated_data.get("password")
        )
        return super(UserRegistrationSerializer, self).create(validated_data)


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий."""

    class Meta:
        model = SubCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""

    subcategory = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'subcategory']


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров."""

    category = serializers.CharField(source='subcategory.category')
    subcategory = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'subcategory', 'price',
                  'images']

    def get_images(self, obj):
        """Формируем список изображения."""
        request = self.context.get('request')
        image_urls = [
            request.build_absolute_uri(obj.image1.url),
            request.build_absolute_uri(obj.image2.url),
            request.build_absolute_uri(obj.image3.url),
        ]
        return image_urls


class CartBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ['product', 'quantity']

    def validate_quantity(self, value):
        """Проверяем, что количество товаров больше 0."""
        if value <= 0:
            raise serializers.ValidationError(
                "Количество товара в корзине должно быть больше 0"
            )
        return value


class CartCreateSerializer(CartBaseSerializer):
    """Сериализатор для добавления товара в корзину."""

    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = ShoppingCart
        fields = ['user', 'product', 'quantity']
        validators = [UniqueTogetherValidator(
            queryset=ShoppingCart.objects.all(), fields=('user', 'product')
        )]

    def to_representation(self, instance):
        """Убираем из ответа поле user."""
        rep = super(CartCreateSerializer, self).to_representation(
            instance
        )
        rep.pop('user')
        return rep


class CartSerializer(CartBaseSerializer):
    """Сериализатор для корзины."""

    product = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['product', 'product_id', 'quantity']


class CartListSerializer(serializers.Serializer):
    """
    Сериализатор для получения информации о всех товаров в корзине
    пользователя.
    """

    products = CartSerializer(many=True)
    total_quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartUpdateSerializer(CartBaseSerializer):
    """Сериализатор для изменения количества товаров в корзине."""


class CartDeleteSerializer(serializers.ModelSerializer):
    """Сериализатор для удаления товара из корзины."""

    class Meta:
        model = ShoppingCart
        fields = ['product']

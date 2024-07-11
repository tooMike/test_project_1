from django.urls import include, path

from api import views

cart = views.CartViewSet.as_view(
    {
        'get': 'list',
        'post': 'create',
        'patch': 'partial_update',
        'delete': 'destroy'
    }
)

cart_clean = views.CartViewSet.as_view(
    {
        'delete': 'clear',
    }
)

urlpatterns = [
    path(
        'categories/',
        views.CategoryViewSet.as_view({'get': 'list'}),
        name='categories'
    ),
    path(
        'products/',
        views.ProductViewSet.as_view({'get': 'list'}),
        name='products'
    ),
    path('cart/', cart, name='cart'),
    path('cart/clean/', cart_clean, name='cart-clean'),
    path(
        'users/',
        views.UserCreateViewSet.as_view({'post': 'create'}),
        name='users'
    ),
    path('auth/', include('djoser.urls.authtoken')),
]

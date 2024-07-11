from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель категории товаров."""

    name = models.CharField(
        max_length=50, verbose_name='Название', unique=True
    )
    slug = models.SlugField(max_length=50, verbose_name='Slug', unique=True)
    image = models.ImageField(upload_to='category', verbose_name='Изображение')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'category'
        ordering = ('name',)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """Модель подкатегории товаров."""

    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, verbose_name='Slug', unique=True)
    image = models.ImageField(
        upload_to='subcategory', verbose_name='Изображение'
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'
        default_related_name = 'subcategory'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара."""

    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, verbose_name='Slug', unique=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена'
    )
    image1 = models.ImageField(
        upload_to='product', verbose_name='Изображение 1'
    )
    image2 = models.ImageField(
        upload_to='product', verbose_name='Изображение 2'
    )
    image3 = models.ImageField(
        upload_to='product', verbose_name='Изображение 3'
    )
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, verbose_name='Подкатегория'
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'
        default_related_name = 'product'
        ordering = ('name',)

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    """Модель корзины."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
        )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
        )
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'
        default_related_name = 'carts'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'product'), name='user_product_unique'
            ),
        ]

    def __str__(self):
        return f'Пользователь: {self.user.username}, товар: {self.product.name}'

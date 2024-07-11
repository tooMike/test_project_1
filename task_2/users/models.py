from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopUser(AbstractUser):
    """Заменяем стандартную модель пользователя на собственную."""

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        default_related_name = 'user'

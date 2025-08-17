from django.db import models
from django.contrib.auth.models import User


class Avatar(models.Model):
    """Модель для хранения аватара пользователя"""

    src = models.ImageField(
        upload_to="avatars/",
        default="avatars/default.jpg",
        verbose_name="Ссылка",
    )
    alt = models.CharField(max_length=128, verbose_name="Аватар")

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    full_name = models.CharField(
        max_length=128,
        blank=True,
        verbose_name='Полное имя'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='Электронная почта'
    )
    balance = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name="Баланс"
    )
    avatar = models.ForeignKey(
        Avatar,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Аватар",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

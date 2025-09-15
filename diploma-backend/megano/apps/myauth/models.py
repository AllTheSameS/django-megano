from django.db import models
from django.contrib.auth.models import User

from megano.settings import DEFAULT_AVATAR_PATH, AVATAR_DOWNLOAD_PATH

from .utils.validators import phone_validator


class Profile(models.Model):
    """
    Модель профиля пользователя

    Attributes:
        user(OneToOneField): Ссылка на модель пользователя.
        full_name(CharField): Полное имя пользователя.
        phone(CharField): Номер телефона.
        email(EmailField): Email адрес.
        balance(DecimalField): Баланс.
        date(DateTimeField): Дата создания профиля.
        updated(DateTimeField): Дата обновления профиля.
    """

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )

    full_name = models.CharField(
        max_length=128,
        blank=True,
        verbose_name='Полное имя',
    )
    phone = models.CharField(
        unique=True,
        max_length=20,
        blank=True,
        verbose_name='Телефон',
    )
    email = models.EmailField(
        unique=True,
        blank=True,
        verbose_name='Электронная почта',
    )
    balance = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0,
        verbose_name="Баланс",
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    def __str__(self):
        return f"Профиль {self.user.username}"


class Avatar(models.Model):
    """
    Модель аватара пользователя.

    Attributes:
        src(ImageField): Изображние.
        alt(CharField): Альтернативный текст изображения.
    """

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"

    src = models.ImageField(
        upload_to=AVATAR_DOWNLOAD_PATH,
        default=DEFAULT_AVATAR_PATH,
        verbose_name="Ссылка",
    )
    alt = models.CharField(
        max_length=128,
        verbose_name="Альтернативный текст",
    )

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='avatar',
        verbose_name='Профиль',
    )

    def __str__(self):
        return self.alt if self.alt else f"Аватар {self.profile.user.username}"

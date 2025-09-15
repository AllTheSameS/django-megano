from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    """
    Модель отзыва.

    Attributes:
        product(ForeignKey): Ссылка на продукт.
        author(ForeignKey): Ссылка на пользователя.
        text(CharField): Текст отзыва.
        rate(FloatField): Рейтинг.
        date(DateTimeField): Дата создания.
        updated(DateTimeField): Дата обновления.
    """
    class Meta:
        ordering = ('-date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    product = models.ForeignKey(
        'goods.Product',
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='reviews_authored',
        verbose_name='Автор',
    )
    text = models.CharField(
        max_length=500,
        blank=False,
        verbose_name='Текст отзыва',
    )
    rate = models.FloatField(
        blank=False,
        null=False,
        db_index=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Рейтинг',
    )
    date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name='Дата создания',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

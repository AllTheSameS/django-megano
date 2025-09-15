from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from megano.settings import (
    DEFAULT_PRODUCT_IMAGE_PATH,
    PRODUCT_IMAGE_DOWNLOAD_PATH,
    )


class Product(models.Model):
    """
    Модель продукта.

    Attributes:
        category(ForeignKey): Ссылка на категорию.
        tags(ManyToManyField): Ссылка на тэги.
        specifications(ManyToManyField): Ссылка на характеристики.
        title(CharField): Название.
        price(DecimalField): Цена.
        count(IntegerField): Количество.
        description(CharField): Описание.
        full_description(TextField): Полное описание.
        free_delivery(BooleanField): Бесплатная доставка.
        rating(FloatField): Рейтинг.
        created(DateTimeField): Дата создания.
        updated(DateTimeField): Дата обновления.
    """
    class Meta:
        ordering = ('title',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        indexes = [
            models.Index(fields=['category', 'price']),
            models.Index(fields=['rating', '-date']),
            models.Index(fields=['free_delivery', 'count']),
        ]

    category = models.ForeignKey(
        'characteristics.Category',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='products',
        verbose_name='Категория',
    )
    tags = models.ManyToManyField(
        'characteristics.Tag',
        blank=True,
        related_name='products',
        verbose_name='Тэги',
    )

    title = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name='Название',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_index=True,
        validators=[MinValueValidator(0)],
        verbose_name='Цена',
    )
    count = models.IntegerField(
        db_index=True,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Количество товара",
    )
    description = models.CharField(
        max_length=128,
        blank=True,
        verbose_name='Описание',
    )
    full_description = models.TextField(
        blank=True,
        verbose_name='Полное описание',
    )
    free_delivery = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name='Бесплатная доставка',
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        db_index=True,
        default=0,
        verbose_name='Рейтинг',
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    available = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='Доступность',
    )
    date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания',

    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """
    Модель изображения продукта.

    Attributes:
        src(ImageField): Изображение.
        alt(CharField): Альтернативный текст.
    """
    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продукта"

    src = models.ImageField(
        upload_to=PRODUCT_IMAGE_DOWNLOAD_PATH,
        default=DEFAULT_PRODUCT_IMAGE_PATH,
        verbose_name="Ссылка",
    )
    alt = models.CharField(
        max_length=128,
        verbose_name="Альтернативный текст",
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Продукт',
    )

    def __str__(self):
        return self.alt if self.alt else "Изображение продукта"

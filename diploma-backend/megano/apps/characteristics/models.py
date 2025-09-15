"""
Модуль работы с моделями характеристик продукта, категориями, тэгами.
"""
from django.db import models

from megano.settings import (
    DEFAULT_CATEGORY_IMAGE_PATH,
    CATEGORY_IMAGE_DOWNLOAD_PATH,
    )

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Модель категории продукта.

    Attributes:
        title(CharField): Название категории.
        parent(ForeignKey): Ссылка на себя.
    """
    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['title']

    title = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Категория",
        )

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родительская категория"
    )

    def __str__(self):
        return self.title


class CategoryImage(models.Model):
    """
    Модель изображения категории.

    Attributes:
        src(ImageField): Изображение.
        alt(CharField): Альтернативный текст.
    """
    class Meta:
        verbose_name = "Изображение категории"
        verbose_name_plural = "Изображения категорий"

    src = models.ImageField(
        upload_to=CATEGORY_IMAGE_DOWNLOAD_PATH,
        default=DEFAULT_CATEGORY_IMAGE_PATH,
        verbose_name="Ссылка",
    )
    alt = models.CharField(
        max_length=128,
        verbose_name="Альтернативный текст",
    )

    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        related_name='image',
        verbose_name='Категория',
    )

    def __str__(self):
        return self.alt if self.alt else "Изображение категории"


class Tag(models.Model):
    """
    Модель тэга продукта.

    Attributes:
        name(CharField): Название тэга.
    """
    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Название тэга",
    )

    def __str__(self):
        return self.name


class Specification(models.Model):
    """
    Модель характеристики продукта.

    Attributes:
        name(CharField): Название характеристики.
    """
    class Meta:
        ordering = ('name',)
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Название характеристики",
        )

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    Модель для связи характеристики с продуктом.

    Attributes:
        product(ForeignKey): Ссылка на продукт.
        specification(ForeignKey): Ссылка на характеристику.
        value(CharField): Значение.
    """
    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товаров'
        unique_together = ('product', 'specification')

    product = models.ForeignKey(
        'goods.Product',
        on_delete=models.CASCADE,
        related_name='specifications_values',
        verbose_name='Товар',
        )
    specification = models.ForeignKey(
        'Specification',
        on_delete=models.CASCADE,
        related_name='product_specs',
        verbose_name='Характеристика',
        )
    value = models.CharField(
        max_length=20,
        verbose_name='Значение',
        )

    def __str__(self):
        return f"{self.specification.name}: {self.value}"

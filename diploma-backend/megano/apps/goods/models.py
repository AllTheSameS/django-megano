from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        verbose_name="Категория",
        )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategory',
        verbose_name="Родительская категория",
    )

    def __str__(self):
        return self.title


class Tag(models.Model):
    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Название тега",
    )

    def __str__(self):
        return self.name


class Specification(models.Model):
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
    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товаров'
        unique_together = ('product', 'specification')

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='specifications_values',
        verbose_name='Товар',
        )
    specification = models.ForeignKey(
        Specification,
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


class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_authored',
        verbose_name='Автор',
    )
    text = models.CharField(
        max_length=500,
        blank=False,
        verbose_name='Текст отзыва',
    )
    rate = models.FloatField(
        blank=True,
        null=True,
        default=None,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Рейтинг',
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Продукт',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )


class Product(models.Model):
    class Meta:
        ordering = ('title',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='products',
        blank=True,
        verbose_name='Тэг',
    )
    specifications = models.ManyToManyField(
        Specification,
        through=ProductSpecification,
        related_name='products',
        verbose_name='Характеристика',
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена',
    )
    count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Количество товара",
    )
    title = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name='Название',
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True,
        verbose_name='Картинка',
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
        default=False,
        verbose_name='Бесплатная доставка',
    )
    rating = models.FloatField(
        default=None,
        blank=True,
        null=True,
        verbose_name='Рейтинг',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',

    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

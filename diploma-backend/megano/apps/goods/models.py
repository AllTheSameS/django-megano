from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from megano.settings import DEFAULT_PRODUCT_IMAGE_PATH, PRODUCT_IMAGE_DOWNLOAD_PATH


class Category(models.Model):
    """
    Модель категории товара.

    Attributes:
        title(CharField): Название категории.
        parent(ForeignKey): Ссылка на себя.
    """
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
    """
    Модель тэга товара.

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
    Модель характеристики.

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
    Модель характеристики товара.

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
    """
    Модель отзыва.

    Attributes:
        author(ForeignKey): Ссылка на пользователя.
        text(CharField): Текст отзыва.
        vratealue(FloatField): Рейтинг.
        product(ForeignKey): Ссылка на товар.
        created(DateTimeField): Дата создания.
        updated(DateTimeField): Дата обновления.
    """
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('author', 'product')

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
        blank=False,
        null=False,
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

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='products',
        verbose_name='Категория',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='products',
        verbose_name='Тэги',
    )
    specifications = models.ManyToManyField(
        Specification,
        through=ProductSpecification,
        related_name='products',
        verbose_name='Характеристики',
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
        validators=[MinValueValidator(0.01)],
        verbose_name='Цена',
    )
    count = models.IntegerField(
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
        db_index=True,
        verbose_name='Дата создания',

    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    def set(self, **kwargs):
        """
        Упрощенная версия set метода для установки полей продукта.
        """
        # Устанавливаем основные поля
        for field, value in kwargs.items():
            if hasattr(self, field):
                field_obj = getattr(self, field)

                # Для ManyToMany полей используем set()
                if isinstance(field_obj, models.ManyToManyField):
                    getattr(self, field).set(value)
                else:
                    setattr(self, field, value)

        self.save()
        return self

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
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Продукт',
    )

    def __str__(self):
        return self.alt if self.alt else "Изображение продукта"

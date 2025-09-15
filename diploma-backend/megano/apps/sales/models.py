from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Sale(models.Model):
    """
    Модель скидки на продукт.

    Attributes:
        sale_price(IntegerField): Цена со скидкой.
        date_from(DateTimeField): Время создания.
        date_to(DateTimeField): Время окончания.
    """
    class Meta:
        ordering = ['date_to']
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_index=True,
        validators=[MinValueValidator(0)],
        verbose_name='Цена',
        )
    date_from = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания',
    )
    date_to = models.DateTimeField(
        db_index=True,
        default=None,
        blank=True,
        verbose_name='Дата оконачания',
    )
    is_active = models.BooleanField(
        db_index=True,
        default=True,
        blank=True,
        verbose_name='Активна',
    )

    def __str__(self):
        return f'{self.products.first().product.title}'


class SaleProduct(models.Model):
    """
    Связная таблица скидок и продуктов.

    Attributes:
        product(ForeignKey): Ссылка на продукт.
        sale(ForeignKey): Ссылка на скидку.
    """
    class Meta:
        ordering = ['id']
        verbose_name = 'Скидка на продукт'
        verbose_name_plural = 'Скидки на продукты'
        unique_together = ['product', 'sale']

    product = models.ForeignKey(
        'goods.Product',
        related_name='sales',
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        )
    sale = models.ForeignKey(
        'Sale',
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Скидка',
    )

    def __str__(self):
        return f"{self.product.title} - {self.sale.sale_price}"

    def clean(self):
        """Валидация для обеспечения только одной активной скидки на продукт"""
        if self.sale and self.sale.is_active:
            active_sales = SaleProduct.objects.filter(
                product=self.product,
                sale__is_active=True
            ).exclude(pk=self.pk)

            if active_sales.exists():
                raise ValidationError(
                    'A product can only have one active sale.'
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
"""
Модуль работы с заказами и элементами заказа.
"""
from django.db import models
from django.contrib.auth.models import User

import uuid


class Order(models.Model):
    """
    Модель заказа.

    Consts:
        DELIVERY_CHOICES: Вариантов доставки.
        PAYMENT_CHOICES: Варианты оплаты.
        STATUS_CHOICES: Статусы заказа.

    Attributes:
        city(CharField): Город.
        address(CharField): Адресс.
        customer(ForeignKey): Ссылка на пользователя.
        date(DateTimeField): Дата создания.
        delivery_type(CharField): Тип доставки.
        payment_type(CharField): Тип оплаты.
        total_cost(DecimalField): Общая стоимость.
        status(CharField): Статус.
        order_number(CharField): Номер заказа.
    """
    DELIVERY_CHOICES = (
        ('ordinary', 'Обычная доставка'),
        ('free', 'Бесплатно'),
        ('express', 'Экспресс-доставка'),
    )

    PAYMENT_CHOICES = (
        ('online', 'Онлайн картой'),
        ('someone', 'Онлайн со случайного чужого счета'),
    )

    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('processing', 'Обработка'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправленный'),
        ('delivered', 'Доставленный'),
        ('cancelled', 'Отменено'),
        ('refunded', 'Возвращено'),
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    city = models.CharField(
        max_length=100,
        null=True,
        default=None,
        verbose_name='Город',
        )

    address = models.CharField(
        max_length=100,
        null=True,
        default=None,
        verbose_name='Адрес',
        )

    customer = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='Клиет',
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    delivery_type = models.CharField(
        db_index=True,
        max_length=20,
        default='ordinary',
        choices=DELIVERY_CHOICES,
        verbose_name='Тип доставки',
    )

    payment_type = models.CharField(
        db_index=True,
        max_length=50,
        default='online',
        choices=PAYMENT_CHOICES,
        verbose_name='Тип оплаты',
    )

    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        default=None,
        verbose_name='Общая стоимость',
    )

    status = models.CharField(
        db_index=True,
        max_length=20,
        default='pending',
        choices=STATUS_CHOICES,
        verbose_name='Статус заказа',
    )

    order_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Номер заказа',
        )

    def __str__(self):
        return f'Order {self.order_number}'

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """
    Модель элементов заказа.

    Attributes:
        order(ForeignKey): Ссылка на заказ.
        product(ForeignKey): Ссылка на продукт.
        count(PositiveIntegerField): Количесво продуктов.
    """
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'goods.Product',
        related_name='order_items',
        on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.count} x {self.product.title}'

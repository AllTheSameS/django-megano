from django.db import models

import uuid


class Payment(models.Model):
    """
    Модель платежа.

    Attributes:
        order(ForeignKey): Ссылка на заказ.
        payment_type(CharField): Тип оплаты.
        total_cost(DecimalField): Общая стоимость.
        status(CharField): Статус.
        transaction_id(CharField): Номер транзакции.
        date(DateTimeField): Дата создания.
    """
    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    PAYMENT_STATUS = [
        ('pending', 'Ожидает оплаты'),
        ('completed', 'Оплачено'),
        ('failed', 'Ошибка оплаты'),
        ('refunded', 'Возврат'),
    ]
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name='Заказ',
    )
    payment_type = models.CharField(
        max_length=50,
        default='online',
        verbose_name='Тип оплаты',
        )
    status = models.CharField(
        max_length=20,
        default='pending',
        verbose_name='Статус',
        choices=PAYMENT_STATUS,
    )
    transaction_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        verbose_name='Номер транзакции',
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    def __str__(self):
        return f'Платеж для заказа №{self.order.order_number}'

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

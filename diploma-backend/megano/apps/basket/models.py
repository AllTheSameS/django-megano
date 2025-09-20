from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Basket(models.Model):
    """
    Модель корзины.

    Attributes:
        user(ForeignKey): Ссылка на пользователя.
        session_key(CharField): Уникальный идентификатор сессии для анонимных пользователей.
        date(DateTimeField): Дата создания.
        updated(DateTimeField): Дата обновления.
    """
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(user__isnull=False),
                name='unique_user_cart'
            ),
            models.UniqueConstraint(
                fields=['session_key'],
                condition=models.Q(user__isnull=True),
                name='unique_session_key_cart'
            )
        ]
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='basket'
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Корзина пользователя {self.user.username}"
        return f"Анонимная корзина ({self.session_key})"

    def get_total_count(self):
        """Общее количество товаров в корзине"""
        return sum(item.count for item in self.items.all())

    def get_total_price(self):
        """Общая стоимость корзины"""
        return sum(item.get_total_price() for item in self.items.all())

    def clear(self):
        """Очистить корзину"""
        self.items.all().delete()

    @classmethod
    def get_or_create_basket(cls, request):
        """
        Метод для получения или создания корзины.
        Работает как для аутентифицированных, так и для анонимных пользователей.
        """
        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key

        if not session_key:
            # Если у запроса еще нет ключа сессии, создаем его
            request.session.create()
            session_key = request.session.session_key

        if user:
            # Ищем корзину пользователя. Если нет - создаем.
            basket, created = cls.objects.get_or_create(user=user)
            # Если у пользователя была корзина из анонимной сессии, можно здесь ее объединить
            anonymous_basket = cls.objects.filter(session_key=session_key, user__isnull=True).first()
            if anonymous_basket:
                # Переносим все items из анонимной корзины в корзину пользователя
                for item in anonymous_basket.items.all():
                    item.move_to_cart(basket)
                anonymous_basket.delete()
                basket.save()
        else:
            # Работаем с анонимной корзиной по session_key
            basket, created = cls.objects.get_or_create(session_key=session_key, user__isnull=True)

        return basket


class BasketItem(models.Model):
    """
    Модель элементов корзины.
    """
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = [['basket', 'product']]
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'goods.Product',
        on_delete=models.CASCADE,
        related_name='basket_items',
    )
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.count} x {self.product.title} в корзине"

    def clean(self):
        """Валидация на уровне модели (опционально, но рекомендуется)"""
        if self.count > self.product.count:
            raise ValidationError(f'Недостаточно товара на складе. Доступно: {self.product.count}')

    def get_total_price(self):
        """Общая стоимость товара в корзине"""
        return self.product.price * self.count

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def move_to_cart(self, target_basket):
        """
        Метод для переноса товара в другую корзину.
        Используется при слиянии анонимной корзины с корзиной пользователя.
        """
        try:
            # Пытаемся найти такой же товар в целевой корзине
            existing_item = BasketItem.objects.get(basket=target_basket, product=self.product)
            existing_item.count += self.count
            existing_item.save()
            self.delete()  # Удаляем старую запись
        except BasketItem.DoesNotExist:
            # Если в целевой корзине такого товара нет, просто меняем привязку
            self.basket = target_basket
            self.save()

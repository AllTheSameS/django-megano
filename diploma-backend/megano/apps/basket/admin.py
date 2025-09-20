from django.contrib import admin
from django.utils.html import format_html
from .models import Basket, BasketItem


class BasketItemInline(admin.TabularInline):
    """Inline для отображения товаров корзины"""
    model = BasketItem
    extra = 0
    readonly_fields = ['product', 'count', 'get_total_price']
    fields = ['product', 'count', 'get_total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Общая стоимость'


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """Админка для корзины"""
    list_display = ['id', 'get_user', 'session_key_short', 'get_total_count', 'get_total_price', 'date', 'updated']
    list_display_links = ['id', 'get_user']
    list_filter = ['date', 'updated']
    search_fields = ['user__username', 'user__email', 'session_key']
    readonly_fields = ['date', 'updated', 'session_key_short']
    inlines = [BasketItemInline]
    fieldsets = [
        ('Основная информация', {
            'fields': ['user', 'session_key_short', 'date', 'updated']
        }),
    ]

    def get_user(self, obj):
        if obj.user:
            return f"{obj.user.username} ({obj.user.email})"
        return "Анонимный пользователь"
    get_user.short_description = 'Пользователь'

    def session_key_short(self, obj):
        if obj.session_key:
            return obj.session_key[:10] + '...' if len(obj.session_key) > 10 else obj.session_key
        return "Нет ключа"
    session_key_short.short_description = 'Ключ сессии (кратко)'

    def get_total_count(self, obj):
        return obj.get_total_count()
    get_total_count.short_description = 'Общее кол-во товаров'

    def get_total_price(self, obj):
        return f"{obj.get_total_price():.2f} руб."
    get_total_price.short_description = 'Общая стоимость'

    def has_add_permission(self, request):
        # Запрещаем создание корзин через админку
        return False


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    """Админка для товаров в корзине"""
    list_display = ['id', 'basket_info', 'product', 'count', 'get_unit_price', 'get_total_price']
    list_display_links = ['id', 'product']
    search_fields = ['product__title', 'basket__user__username', 'basket__session_key']
    readonly_fields = ['get_unit_price', 'get_total_price']
    fields = ['basket', 'product', 'count', 'get_unit_price', 'get_total_price']

    def basket_info(self, obj):
        if obj.basket.user:
            return f"Корзина {obj.basket.user.username}"
        return f"Анонимная корзина ({obj.basket.session_key[:10]}...)"
    basket_info.short_description = 'Корзина'

    def get_unit_price(self, obj):
        return f"{obj.product.price:.2f} руб."
    get_unit_price.short_description = 'Цена за единицу'

    def get_total_price(self, obj):
        return f"{obj.get_total_price():.2f} руб."
    get_total_price.short_description = 'Общая стоимость'

    def has_add_permission(self, request):
        # Запрещаем создание товаров корзины через админку
        return False

from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админка для модели Order"""

    list_display = (
        'order_number',
        'customer',
        'city',
        'total_cost',
        'status',
        'delivery_type',
        'payment_type',
        'date',
    )

    list_filter = (
        'status',
        'delivery_type',
        'payment_type',
        'date',
    )

    search_fields = (
        'order_number',
        'customer__username',
        'city',
        'address',
    )

    readonly_fields = ('order_number', 'date')

    fieldsets = (
        ('Основная информация', {
            'fields': ('order_number', 'customer', 'date', 'total_cost', 'status')
        }),
        ('Доставка', {
            'fields': ('delivery_type', 'city', 'address')
        }),
        ('Оплата', {
            'fields': ('payment_type',)
        }),
    )


class OrderItemInline(admin.TabularInline):
    """Inline для отображения элементов заказа"""
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'count')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Админка для модели OrderItem"""

    list_display = ('order', 'product', 'count')
    list_filter = ('order__status',)
    search_fields = (
        'order__order_number',
        'product__title'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# Добавляем inline к OrderAdmin
OrderAdmin.inlines = [OrderItemInline]

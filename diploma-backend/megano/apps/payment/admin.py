from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Payment.
    """
    list_display = ('transaction_id', 'order', 'payment_type', 'status', 'date')
    list_filter = ('status', 'payment_type', 'date')
    search_fields = ('transaction_id', 'order__order_number')
    readonly_fields = ('date', 'transaction_id')
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('order', 'payment_type', 'status')
        }),
        ('Детали транзакции', {
            'fields': ('transaction_id', 'date')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Делаем transaction_id редактируемым только при создании.
        """
        if obj:  # объект уже существует (редактирование)
            return self.readonly_fields + ('transaction_id',)
        return self.readonly_fields
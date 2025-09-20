from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Административная панель для модели отзывов.
    """
    list_display = ('product', 'author', 'rate', 'date', 'updated')
    list_filter = ('rate', 'date', 'updated', 'product')
    search_fields = ('text', 'author__username', 'product__name')
    readonly_fields = ('date', 'updated')
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('product', 'author', 'rate')
        }),
        ('Содержание отзыва', {
            'fields': ('text',)
        }),
        ('Даты', {
            'fields': ('date', 'updated'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'author')
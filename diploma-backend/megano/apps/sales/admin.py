from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Sale, SaleProduct


class SaleProductInline(admin.TabularInline):
    """
    Inline для отображения продуктов со скидкой
    """
    model = SaleProduct
    extra = 1
    verbose_name = 'Продукт со скидкой'
    verbose_name_plural = 'Продукты со скидкой'


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Административная панель для модели скидок.
    """
    list_display = ('sale_price', 'date_from', 'date_to', 'is_active', 'products_count')
    list_filter = ('is_active', 'date_from', 'date_to')
    search_fields = ('products__product__title', 'sale_price')
    readonly_fields = ('date_from',)
    list_editable = ('is_active',)
    list_per_page = 20

    fieldsets = (
        ('Информация о скидке', {
            'fields': ('sale_price', 'is_active')
        }),
        ('Период действия', {
            'fields': ('date_from', 'date_to'),
            'classes': ('collapse',)
        }),
    )

    inlines = [SaleProductInline]

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество продуктов'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products')


@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    """
    Административная панель для связи продуктов и скидок.
    """
    list_display = ('product', 'sale', 'sale_price_display', 'price_display', 'is_active_display')
    list_filter = ('sale__is_active', 'sale__date_from', 'sale__date_to')
    search_fields = ('product__title', 'sale__sale_price')
    list_per_page = 20

    def sale_price_display(self, obj):
        return obj.sale.sale_price
    sale_price_display.short_description = 'Цена со скидкой'

    def price_display(self, obj):
        return obj.product.price
    price_display.short_description = 'Цена без скидкой'

    def is_active_display(self, obj):
        return obj.sale.is_active
    is_active_display.short_description = 'Активна'
    is_active_display.boolean = True

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'sale')

    def clean_model(self, request, obj, form, change):
        """
        Валидация при сохранении через админку
        """
        if obj.sale and obj.sale.is_active:
            active_sales = SaleProduct.objects.filter(
                product=obj.product,
                sale__is_active=True
            ).exclude(pk=obj.pk)

            if active_sales.exists():
                raise ValidationError(
                    'Продукт может иметь только одну активную скидку.'
                )

    def save_model(self, request, obj, form, change):
        self.clean_model(request, obj, form, change)
        super().save_model(request, obj, form, change)
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """
    Inline для отображения изображений продукта в админке.
    """
    model = ProductImage
    extra = 1
    fields = ('src', 'alt', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.src:
            return format_html('<img src="{}" height="100" />', obj.src.url)
        return "Нет изображения"
    image_preview.short_description = 'Предпросмотр'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админка для модели Product.
    """
    list_display = (
        'title', 
        'category', 
        'price', 
        'count', 
        'rating', 
        'free_delivery', 
        'limited_edition',
        'available',
        'date'
    )
    list_filter = (
        'category',
        'free_delivery',
        'limited_edition',
        'available',
        'date',
        'rating'
    )
    search_fields = ('title', 'description', 'full_description')
    list_editable = ('price', 'count', 'available', 'free_delivery')
    list_per_page = 20
    inlines = [ProductImageInline]
    readonly_fields = ('date', 'updated', 'rating', 'shopping_counter')
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title', 
                'category', 
                'tags',
                'price', 
                'count',
                'shopping_counter',
                'rating'
            )
        }),
        ('Описание', {
            'fields': (
                'description', 
                'full_description'
            )
        }),
        ('Дополнительно', {
            'fields': (
                'free_delivery',
                'limited_edition',
                'available',
                'date',
                'updated'
            )
        }),
    )
    filter_horizontal = ('tags',)

    def get_readonly_fields(self, request, obj=None):
        """
        Делаем рейтинг и счетчик покупок только для чтения.
        """
        if obj:
            return self.readonly_fields + ('rating', 'shopping_counter')
        return self.readonly_fields


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Админка для модели ProductImage.
    """
    list_display = ('product', 'alt', 'image_preview')
    list_filter = ('product',)
    search_fields = ('product__title', 'alt')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.src:
            return format_html('<img src="{}" height="150" />', obj.src.url)
        return "Нет изображения"
    image_preview.short_description = 'Предпросмотр'

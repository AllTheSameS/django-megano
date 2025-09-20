from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from .models import Category, CategoryImage, Tag, Specification, ProductSpecification


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админка для категорий с поддержкой древовидной структуры
    """
    list_display = ('tree_actions', 'indented_title', 'products_count')
    list_display_links = ('indented_title',)
    search_fields = ('title',)
    ordering = ('tree_id', 'level', 'title')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products')

    def products_count(self, instance):
        return instance.products.count()
    products_count.short_description = 'Количество товаров'


@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    """
    Админка для изображений категорий
    """
    list_display = ('alt', 'category', 'image_preview')
    list_filter = ('category',)
    search_fields = ('alt', 'category__title')

    def image_preview(self, obj):
        if obj.src:
            return format_html('<img src="{}" height="50" />', obj.src.url)
        return "Нет изображения"
    image_preview.short_description = 'Превью'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Админка для тегов
    """
    list_display = ('name', 'products_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products')

    def products_count(self, instance):
        return instance.products.count()
    products_count.short_description = 'Количество товаров'


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    """
    Админка для характеристик
    """
    list_display = ('name', 'products_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('product_specs')

    def products_count(self, instance):
        return instance.product_specs.count()
    products_count.short_description = 'Количество применений'


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    """
    Админка для связей товаров и характеристик
    """
    list_display = ('product', 'specification', 'value')
    list_filter = ('specification',)
    search_fields = ('product__name', 'specification__name', 'value')
    autocomplete_fields = ('product', 'specification')

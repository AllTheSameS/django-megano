from django.contrib import admin
from .models import Category, Product


from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Tag, Specification, ProductSpecification, 
    Review, Product, ProductImage
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'products_count')
    list_filter = ('parent',)
    search_fields = ('title',)
    ordering = ('title',)

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество товаров'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'products_count')
    search_fields = ('name',)
    ordering = ('name',)

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество товаров'


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'products_count')
    search_fields = ('name',)
    ordering = ('name',)

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество товаров'


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    verbose_name = 'Характеристика товара'
    verbose_name_plural = 'Характеристики товара'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    verbose_name = 'Изображение'
    verbose_name_plural = 'Изображения'
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.src:
            return format_html('<img src="{}" height="50" />', obj.src.url)
        return "Нет изображения"
    image_preview.short_description = 'Превью'


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('author', 'rate', 'created', 'updated')
    can_delete = False
    verbose_name = 'Отзыв'
    verbose_name_plural = 'Отзывы'

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'price', 'count', 
        'rating', 'free_delivery', 'created'
    )
    list_filter = ('category', 'tags', 'free_delivery', 'created')
    search_fields = ('title', 'description', 'full_description')
    readonly_fields = ('rating', 'created', 'updated')
    filter_horizontal = ('tags',)
    ordering = ('title',)
    list_per_page = 25

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'category', 'tags', 'price', 'count')
        }),
        ('Описание', {
            'fields': ('description', 'full_description'),
            'classes': ('collapse',)
        }),
        ('Дополнительно', {
            'fields': ('free_delivery', 'rating', 'created', 'updated'),
            'classes': ('collapse',)
        }),
    )

    inlines = [ProductSpecificationInline, ProductImageInline, ReviewInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'tags', 'category', 'reviews'
        )


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'specification', 'value')
    list_filter = ('specification',)
    search_fields = ('product__title', 'specification__name', 'value')
    list_select_related = ('product', 'specification')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'rate', 'created', 'updated')
    list_filter = ('rate', 'created')
    search_fields = ('product__title', 'author__username', 'text')
    readonly_fields = ('created', 'updated')
    list_select_related = ('product', 'author')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'author')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt', 'image_preview')
    list_filter = ('product__category',)
    search_fields = ('product__title', 'alt')
    list_select_related = ('product',)

    def image_preview(self, obj):
        if obj.src:
            return format_html('<img src="{}" height="50" />', obj.src.url)
        return "Нет изображения"
    image_preview.short_description = 'Превью'
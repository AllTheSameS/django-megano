from django.contrib import admin
from .models import Category, Product


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['title',]


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['title', 'tag', 'price', 'created', 'updated',]
#     list_filter = ['available', 'category', 'created', 'updated',]
#     list_editable = ['price', 'available', 'discount',]
#     prepopulated_fields = {'slug': ('title',)}
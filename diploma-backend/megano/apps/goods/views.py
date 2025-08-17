from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .models import Tag, Product


def product_list(request, category_slag=None):
    categories = Tag.objects.all()
    products = Product.objects.filter(available=True)

    category = None
    if category_slag:
        category = get_object_or_404(Tag, category_slag=category_slag)
        products = products.filter(category=category)
    return render(request, 'frontend/catalog.html', {
        'category': category,
        'categories': categories,
        'products': products,
        })


# class ProductList(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [
#         SearchFilter,
#         DjangoFilterBackend,
#         OrderingFilter,
#     ]
#     search_fields = ("name", "description",)
#     filterset_fields = (
#         "name",
#         "description",
#         "price",
#         "discount",
#     )
#     ordering_fields = [
#         "name",
#         "price",
#         "discount",
#     ]

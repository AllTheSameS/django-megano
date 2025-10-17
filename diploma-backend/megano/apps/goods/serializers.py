from typing import Any
from apps.characteristics.serializers import GetTagsSerializer, SpecificationSerializer, TagSerializer
from rest_framework import serializers

from .models import Product, ProductImage
from apps.reviews.serializers import ReviewSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    """Сериализация атрибутов изображения продукта."""
    class Meta:
        model = ProductImage
        fields = ("src", "alt")


class ProductDetailSerializer(serializers.ModelSerializer):
    """Подробное представление продукта с вложенными отношениями и вычисляемыми полями."""
    specifications = serializers.SerializerMethodField()
    fullDescription = serializers.CharField(source="full_description")
    freeDelivery = serializers.BooleanField(source="free_delivery")
    reviews = ReviewSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "tags",
            "reviews",
            "specifications",
            "rating",
            "images",
            "available",
        )

    def get_specifications(self, obj: Product) -> list[dict]:
        product_specs = obj.specifications_values.all()
        return SpecificationSerializer(product_specs, many=True).data

    def get_price(self, obj: Product) -> Any:
        return obj.get_price()


class ProductSerializer(serializers.ModelSerializer):
    """Компактное представление продукта, подходящее для списков."""
    reviews = serializers.SerializerMethodField()
    freeDelivery = serializers.BooleanField(source="free_delivery")
    tags = GetTagsSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "title",
            "price",
            "freeDelivery",
            "reviews",
            "images",
            "tags",
            "count",
            "description",
            "date",
            "rating",
        )

    def get_reviews(self, obj: Product) -> int:
        return obj.reviews.count() if hasattr(obj, "reviews") else 0

    def get_price(self, obj: Product) -> Any:
        return obj.get_price()

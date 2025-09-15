from rest_framework import serializers

from .models import Product, ProductImage

from apps.characteristics.serializers import TagSerializer, GetTagsSerializer, SpecificationSerializer
from apps.reviews.serializers import ReviewSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['src', 'alt']


class ProductDetailSerializer(serializers.ModelSerializer):
    specifications = serializers.SerializerMethodField()
    fullDescription = serializers.CharField(source="full_description")
    freeDelivery = serializers.BooleanField(source="free_delivery")
    reviews = ReviewSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "category", "price", "count", "date", "title",
            "description", "fullDescription", "freeDelivery", "tags",
            "reviews", "specifications", "rating", "images", "available",
        ]

    def get_specifications(self, obj):
        product_specs = obj.specifications_values.all()
        return SpecificationSerializer(product_specs, many=True).data

    def get_price(self, obj):
        return obj.sales.first().sale.sale_price if obj.sales.first() else obj.price


class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    freeDelivery = serializers.BooleanField(source="free_delivery")
    tags = GetTagsSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'title',
            'price', 'freeDelivery', 'reviews',
            'images', 'tags', 'count',
            'description', 'date', 'rating',
            ]

    def get_reviews(self, obj):
        return obj.reviews.count() if hasattr(obj, 'reviews') else 0

    def get_price(self, obj):
        return obj.sales.first().sale.sale_price if obj.sales.first() else obj.price

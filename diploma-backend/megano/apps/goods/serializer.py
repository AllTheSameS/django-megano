from rest_framework import serializers

from .models import Product, Review, ProductImage, ProductSpecification, Tag


class SpecificationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='specification.name')
    value = serializers.CharField()

    class Meta:
        model = ProductSpecification
        fields = ['name', 'value']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name',]


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    date = serializers.DateTimeField(source='created', format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Review
        fields = ['id', 'author', 'text', 'rate', 'date']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['text', 'rate', 'product', 'author']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['src', 'alt']


class ProductDetailSerializer(serializers.ModelSerializer):
    specifications = serializers.SerializerMethodField()
    date = serializers.DateTimeField(source='created')
    fullDescription = serializers.CharField(source="full_description")
    freeDelivery = serializers.BooleanField(source="free_delivery")
    reviews = ReviewSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "category", "price", "count", "date", "title",
            "description", "fullDescription", "freeDelivery", "tags",
            "reviews", "specifications", "rating", "images",
        ]

    def get_specifications(self, obj):
        product_specs = obj.specifications_values.all()
        return SpecificationSerializer(product_specs, many=True).data

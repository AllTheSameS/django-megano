from rest_framework import serializers

from apps.goods.models import Product
from apps.goods.serializers import ProductImageSerializer
from apps.characteristics.serializers import TagSerializer


class BannerSerializer(serializers.ModelSerializer):
    freeDelivery = serializers.BooleanField(source="free_delivery")
    images = ProductImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()
    category = serializers.IntegerField(source="category.id", read_only=True)
    date = serializers.DateTimeField(format="%a %b %d %Y %H:%M:%S GMT%z")
    reviews = serializers.IntegerField(source='reviewsCount', read_only=True)

    class Meta:
        model = Product
        fields = ["id", "category", "price", "count", "date", "title",
            "description", "freeDelivery", "tags", "reviews", "rating", "images",
        ]

    def get_price(self, obj):
        return obj.get_price()

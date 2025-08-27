from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    date = serializers.CharField(source='create_at', max_length=128)
    fullDescription = serializers.CharField(source="full_description")
    freeDelivery = serializers.BooleanField(source="free_delivery")

    class Meta:
        model = Product
        fields = ["category", "price", "count",
                  "date", "title", "description", "fullDescription",
                  "freeDelivery", "tags", "reviews", "specifications", "rating"]

from rest_framework import serializers

from .models import BasketItem

from apps.goods.serializers import ProductImageSerializer
from apps.characteristics.serializers import GetTagsSerializer


class BasketItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="product.id", read_only=True)
    title = serializers.CharField(source='product.title')
    images = ProductImageSerializer(source='product.images', many=True, read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = BasketItem
        fields = ['id',  'title', 'images', 'count', 'price']

    def get_price(self, obj):
        return obj.product.sales.first().sale.sale_price if obj.product.sales.first() else obj.product.price


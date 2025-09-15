from rest_framework import serializers

from .models import Sale

from apps.goods.serializers import ProductImageSerializer


class SaleProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    title = serializers.CharField(source='product.title')
    images = ProductImageSerializer(many=True, read_only=True, source='product.images')
    salePrice = serializers.DecimalField(source='sale.sale_price', max_digits=10, decimal_places=2)
    dateFrom = serializers.DateTimeField(source='sale.date_from', format='%d-%m')
    dateTo = serializers.DateTimeField(source='sale.date_to', format='%d-%m')
    class Meta:
        model = Sale
        fields = ['id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images']
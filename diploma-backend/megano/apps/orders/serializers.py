from rest_framework import serializers

from apps.goods.serializers import ProductImageSerializer

from .models import OrderItem, Order



class OrderItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title')
    images = ProductImageSerializer(source='product.images', many=True, read_only=True)
    price = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id',  'title', 'images', 'count', 'price']

    def get_price(self, obj):
        return obj.product.get_price()


class OrderSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source='date', format='%Y-%m-%d %H:%M:%S')
    fullName = serializers.CharField(source='customer.username', read_only=True)
    email = serializers.EmailField(source='customer.profile.email', read_only=True)
    phone = serializers.CharField(source='customer.profile.phone', read_only=True)
    deliveryType = serializers.CharField(source='delivery_type')
    paymentType = serializers.CharField(source='payment_type')
    totalCost = serializers.DecimalField(source='total_cost',
                                         max_digits=10,
                                         decimal_places=2)
    products = OrderItemSerializer(source='items', many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'city', 'address', 'createdAt', 'fullName', 'email', 'phone', 'deliveryType', 'paymentType', 'totalCost',
                  'status', 'products']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.method == 'POST':
            if 'id' in data:
                data['orderId'] = data.pop('id')
        return data

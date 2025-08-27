from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product
from .serializer import ProductSerializer


class ProductDetailsView(APIView):
    """
    Получение продукта.
    """
    def get(self, request, id: int):
        print(request, id)
        product = Product.objects.filter(pk=id)
        print(product)
        serializer = ProductSerializer(product)
        print(serializer.is_valid())

        return Response(product)
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.goods.models import Product

from .models import Basket, BasketItem
from .serializers import BasketItemSerializer


class BasketView(APIView):
    """
    Представление работы с корзиной.
    """
    def get(self, request):
        """
        GET /basket

        Метод получения продуктов в корзине.
        """
        try:
            basket = Basket.get_or_create_basket(request)
            products = [item for item in basket.items.all()]
            serializer = BasketItemSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK,)
        except Exception:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """
        POST /basket

        Метод добавления товаров в корзину.
        """
        try:
            id = request.data['id']
            count = request.data['count']
            product = get_object_or_404(Product, id=id, available=True)
            basket = Basket.get_or_create_basket(request)
            try:
                item = BasketItem.objects.get(basket=basket, product=product)
                item.count += count
                item.save()
            except BasketItem.DoesNotExist:
                BasketItem.objects.create(basket=basket, product=product, count=count)
            serializer = BasketItemSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK,)

        except Exception:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request):
        try:
            id = request.data['id']
            count = request.data['count']

            product = get_object_or_404(Product, id=id, available=True)
            basket = Basket.get_or_create_basket(request)
            try:
                item = BasketItem.objects.get(basket=basket, product=product)
                item.count -= count
                if not item.count:
                    item.delete()
                else:
                    item.save()
            except BasketItem.DoesNotExist:
                return Response(
                    {'error': 'This product does not exist.'},
                    status=status.HTTP_404_NOT_FOUND,
                    )
            serializer = BasketItemSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK,)

        except Exception:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

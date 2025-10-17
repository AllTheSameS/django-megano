"""
Модуль работы с заказами.

Views:
    OrderView()
        Представление работы с заказами.

    OrderDetailView()
        Представление работы с заказами по id.

"""
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


from apps.goods.models import Product
from apps.basket.models import Basket

from .models import Order, OrderItem
from .serializers import OrderSerializer


from apps.utils.utils import BaseView

import logging

logger = logging.getLogger('orders')


class OrderView(APIView, BaseView, LoginRequiredMixin):
    """
    Представление работы с заказами.

    Methods:
        get: Метод получения всех заказов.
        post: Метод добавления заказа.
    """
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        GET /orders

        Метод получения всех заказов.

        Attributes:
            request: Метаданные запроса.
        """
        try:
            logger.info('User %s receives orders.', request.user)
            orders = self._get_user_orders(user=request.user)
            serializer = OrderSerializer(orders, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )

    def post(self, request):
        """
        POST /orders

        Метод добавления заказа.

        Attributes:
            request: Метаданные запроса.
        """

        try:
            logger.info('User %s adds an order.', request.user)

            self._check_list_products(data=request.data)
            order = self._get_or_create_order(user=request.user)
            self._adding_products_to_order(data=request.data, order=order)

            order.calculation_total_cost()
            order.delivery_calculation()
            order.save()
            Basket.objects.filter(user=request.user).delete()
            return Response(
                {"orderId": order.id},
                status=status.HTTP_201_CREATED,
                )

        except Product.DoesNotExist as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_404_NOT_FOUND,
                logger=logger,
            )
        except KeyError as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_400_BAD_REQUEST,
                logger=logger,
            )
        except ValueError as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_400_BAD_REQUEST,
                logger=logger,
            )
        except Exception as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )

    def _adding_products_to_order(self, data, order):
        """
        Добавление продуктов в заказ.

        Attributes:
            data: Данные о продукте(id, количество).
            order: Заказ.
        """
        for item_data in data:
            product_id = item_data.get('id')
            count = item_data.get('count')
            product = Product.objects.get(pk=product_id)
            if not product:
                raise Product.DoesNotExist('Product with id {product_id} not found.')

            if not product.checking_count_goods(count=count):
                raise ValueError(f'Invalid count for product {product_id}')
            OrderItem.objects.create(
                order=order,
                product=product,
                count=count,
            )

    def _get_user_orders(self, user):
        """
        Вспомогательный метод получения заказов пользователя.

        Attributes:
            user: Пользователь.
        """
        logger.debug('Get user orders.')
        return Order.objects.filter(customer=user)

    def _get_or_create_order(self, user):
        """
        Получение или создание заказа.

        Attributes:
            user: Пользователь.
        """
        try:
            order = Order.objects.get(
                customer=user,
                status='pending'
                )
            logger.debug('Get user order: %s.', order)
        except Order.DoesNotExist:
            order = Order.objects.create(
                customer=user,
            )
            logger.debug('Create user order: %s.', order)
        return order

    def _check_list_products(self, data):

        """
        Проверка на не пустой список товаров.

        Attributes:
            data: Список товаров.
        """
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError('Expected non-empty list of products.')


class OrderDetailView(APIView):
    """
    Представление работы с заказами по id.
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id: int):
        """
        Метод получения заказа по id.

        Attributes:
            request: Метаданные запроса.
            id(int): Id заказа.
        """
        try:
            order = Order.objects.get(pk=id)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    def post(self, request, id: int):
        """
        POST /order/{id}

        Метод подтверждения заказа.

        Attributes:
            request: Метаданные запроса.
            id(int): Id заказа.
        """
        try:
            order = Order.objects.get(pk=id)
            serializer = OrderSerializer(order, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

"""
Модуль представлений приложения "basket".

Views:
    BasketView()
        Представление работы с корзиной.
"""

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.goods.models import Product

from .models import Basket, BasketItem
from .serializers import BasketItemSerializer

from apps.utils.utils import BaseView

import logging


logger = logging.getLogger('basket')


class BasketView(APIView, BaseView):
    """
    Представление работы с корзиной.

    Methods:
        get: Метод получения продуктов в корзине.
        post: Метод добавления товаров в корзину.
        delete: Метод удаление товара из корзины.
        _get_product: Вспомогательный метод получения продукта по id.
        _add_product_to_basket: Вспомогательный метод добавление продукта из корзины.
        _delete_product_from_basket: Вспомогательный метод удаление продукта из корзины.
        _get_basket: Вспомогательный метод получение корзины пользователя.
        _get_basket_items: Вспомогательный метод получение объектов корзины.
        _build_response: Построение ответа.
        _handle_error: Построение ответа ошибки.
    """
    def get(self, request):
        """
        GET /basket

        Метод получения продуктов в корзине.

        Attributes:
            request: Метаданные запроса.
        """
        try:
            logger.info('Get products in basket.')
            basket = self._get_basket(request)
            products = self._get_basket_items(basket)
            return self._build_response(
                data=products,
                serializer=BasketItemSerializer,
                status=status.HTTP_200_OK,
                logger=logger,
                many=True,
                )
        except Exception as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )

    def post(self, request):
        """
        POST /basket

        Метод добавления товаров в корзину.

        Attributes:
            request: Метаданные запроса.
        """
        try:
            id = request.data['id']
            count = request.data['count']

            logger.info('User: %s adds to basket product: %s count: %s', request.user, id, count)
            product = self._get_product(id)
            basket = self._get_basket(request)
            self._add_product_to_basket(
                basket=basket,
                product=product,
                count=count,
                )
            return self.get(request)

        except Exception as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )

    def delete(self, request):
        """
        Удаление товара из корзины.

        Attributes:
            request: Метаданные запроса.
        """
        try:
            id = request.data['id']
            count = request.data['count']
            logger.info('User: %s delete from basket product: %s count: %s', request.user, id, count)
            product = self._get_product(id)
            basket = self._get_basket(request)
            self._delete_product_from_basket(
                basket=basket,
                product=product,
                count=count,
            )
            return self.get(request)

        except Exception as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )

    def _get_product(self, id):
        """
        Вспомогательный метод получения продукта по id.

        Attributes:
            id(int): Id продукта.
        """
        logger.debug('Get product %s', id)
        return get_object_or_404(Product, id=id, available=True)

    def _add_product_to_basket(self, basket, product, count):
        """
        Вспомогательный метод добавление продукта из корзины.

        Attributes:
            basket: Корзина.
            product: Продукт.
            count: Количество.
        """
        logger.debug('User: %s adds to basket product: %s count: %s', basket.user, id, count)
        try:
            item = BasketItem.objects.get(basket=basket, product=product)
            item.count += count
            item.save()
        except BasketItem.DoesNotExist:
            BasketItem.objects.create(basket=basket, product=product, count=count)

    def _delete_product_from_basket(self, basket, product, count):
        """
        Вспомогательный метод удаление продукта из корзины.

        Attributes:
            basket: Корзина.
            product: Продукт.
            count: Количество.
        """
        logger.debug('User: %s delete from basket product: %s count: %s', basket.user, id, count)
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

    def _get_basket(self, request):
        """
        Вспомогательный метод получение корзины пользователя.

        Attributes:
            request: Метаданные запроса.
        """
        logger.debug("Get %s basket: ", request.user)
        return Basket.get_or_create_basket(request)

    def _get_basket_items(self, basket):
        """
        Вспомогательный метод получение объектов корзины.

        Attributes:
            basket: Корзина.
        """
        logger.debug("Get basket items: %s", basket.user)
        return list(basket.items.all())

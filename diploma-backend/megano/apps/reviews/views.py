from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from apps.goods.models import Product
from apps.utils.utils import BaseView

from .serializers import ReviewCreateSerializer
from .models import Review

import logging

logger = logging.getLogger('reviews')


class ReviewView(APIView, BaseView):
    """
    Представление работы с отзывами продукта.

    Methods:
        post()
            Метод создания отзыва о продукте по ID.

        _get_product()
            Вспомогательный метод получения продукта по ID.

        _review_check()
            Проверка на уже созданный отзыв пользователя на продукт.

        _update_product_rating()
            Обновление рейтинга продукта на основе всех отзывов.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        """
        POST /product/<int:id>/reviews

        Метод создания отзыва о продукте по ID.

        Attributes:
            request: Метаданные запроса.
            id(int): ID продукта.
        """
        try:
            logger.info('User %s leaves a review for the product %s', request.user.id, id)
            product = self._get_product(id=id)
            self._review_check(
                product=product,
                user=request.user,
            )

            request.data['product'] = id
            request.data['author'] = request.user.id
            serializer = ReviewCreateSerializer(data=request.data)

            if serializer.is_valid():
                print(product.rating)
                product.update_product_rating()
                print(product.rating)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
                return self._handle_error(
                    message=str(e),
                    status=status.HTTP_400_BAD_REQUEST,
                    logger=logger,
                )
        except Product.DoesNotExist as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_404_NOT_FOUND,
                logger=logger,
            )
        except Exception as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )

    def _get_product(self, id: int):
        """
        Вспомогательный метод получения продукта по ID.

        Attributes:
            id(int): Id продукта.
        """
        logger.debug('Get product.')
        return Product.objects.get(pk=id)

    def _review_check(self, product, user):
        """
        Проверка на уже созданный отзыв пользователя на продукт.

        Attributes:
            product: Продукт.
            user: Пользователь.
        """
        logger.debug('User %s has already left a review for this product %s.', user.id, id)
        if product.reviews.filter(author=user).exists():
            raise ValueError('You have already left a review for this product.')

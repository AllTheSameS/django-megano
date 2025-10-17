
"""
Модуль представлений приложения "banners".

Views:
    BannerView()
        Предствление работы с банером сайта.
"""

from rest_framework.views import APIView
from rest_framework import status

from django.db.models import Count

from .serializers import BannerSerializer

from apps.goods.models import Product
from apps.utils.utils import BaseView

import logging

logger = logging.getLogger('banners')


class BannerView(APIView, BaseView):
    """
    Предствление работы с банером сайта.

    Methods:
        get: Метод получения банера.
        _get_products: Вспомогательный метод получения продуктов.
    """

    def get(self, request):
        """
        GET /banners

        Метод получения банера.

        Attributes:
            request: Метаданные запроса.
        """
        try:
            logger.info('Get banners.')
            products = self._get_products()
            return self._build_response(
                data=products,
                serializer=BannerSerializer,
                status=status.HTTP_200_OK,
                logger=logger,
                many=True,
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

    def _get_products(self):
        """
        Вспомогательный метод получения продуктов.
        """
        logger.debug('Get banners.')
        return Product.objects.select_related('category').prefetch_related(
                    'tags',
                    'specifications_values__specification',
                    'reviews',
                    'images'
                ).filter(available=True, count__gte=1).annotate(reviewsCount=Count('reviews'))[:5]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.utils.utils import BaseView

from .models import SaleProduct
from .serializers import SaleProductSerializer

import logging

logger = logging.getLogger('sales')


class SalesView(APIView, BaseView):
    """
    Представление работы с продуктами со скидкой.
    """
    def get(self, request):
        """
        GET /sales

        Метод получения продуктов со скидкой.

        Attributes:
            request: Метаданные запроса.
        """
        try:
            logger.info('Get sales.')
            sale_products = self._get_sale_products()
            page = int(request.GET.get('currentPage', 1))
            limit = int(request.GET.get('limit', 20))

            paginator, page_obj = self._create_paginator(
                products=sale_products,
                page=page,
                limit=limit,
                )
            serializer = SaleProductSerializer(page_obj.object_list, many=True)
            return Response({
                'items': serializer.data,
                'currentPage': page_obj.number,
                'lastPage': paginator.num_pages,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )

    def _get_sale_products(self):
        """
        Вспомогательный метод получения скидок.
        """
        logger.debug('Get sales.')
        return SaleProduct.objects.select_related('product').filter(sale__is_active=True)

    def _create_paginator(self, products, page, limit):
        """
        Создание пагинатора.

        Attributes:
            products: Список продуктов.
            page: Страница.
            limit: Лимит страниц.
        """
        logger.debug('Create paginator.')
        paginator = Paginator(products, limit)
        result_page = ''
        try:
            page = paginator.page(page)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return paginator, result_page
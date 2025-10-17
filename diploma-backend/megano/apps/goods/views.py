"""
Модуль представлений приложения "goods".

Views:
    ProductView()
        Представление работы с каталогом.

    ProductDetailsView()
        Предствление работы с детальной информацией продукта.

    ProductPopularView()
        Представление работы с популярными продуктами.

    ProductLimitedView()
        Представление работы с продуктами.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count, Value, IntegerField, Min, F, Q
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import  Product
from .serializers import ProductDetailSerializer, ProductSerializer
from .utils.filter_and_sort_catalog import ProductFilterService

from apps.utils.utils import BaseView

import logging


logger = logging.getLogger('goods')


class ProductView(APIView, BaseView):
    """
    Представление работы с каталогом.

    CONSTS:
        DEFAULT_PAGE(int): Текущая страница.
        DEFAULT_LIMIT(int): Лимит страниц.

    Methods:
        get(request)
            Основной метод получения продуктов.

        _get_filtered_products(request)
            Вспомогательный метод получения продуктов.
            Фильтрует и сортирует продукты.

        _paginate_products(request, products)
            Метод пагинации.

        _build_response(data)
            Метод построение ответа.

        _handle_error(message, error, status)
            Метод ответа ошибки.

    """
    DEFAULT_PAGE = 1
    DEFAULT_LIMIT = 20

    def get(self, request):
        """
        GET /catalog

        Метод получения продуктов по фильтрам.

        Attributes:
            request: Метаданные запроса.
        """
        try:
            logger.info('Get all products.')
            products = self._get_filtered_and_sorted_products(
                request=request,
                )
            paginated_data = self._paginate_products(
                request=request,
                products=products,
                )
            return self._build_response(
                data=paginated_data,
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

    def _get_filtered_and_sorted_products(self, request):
        """
        Фильтрация и сортировка продуктов.

        Attributes:
            request: Метаданные запроса.
        """
        logger.debug('Filtration and sorting of products.')
        filters = ProductFilterService.build_filters(request.GET)
        products = Product.objects.annotate(
                reviews_count=Coalesce(Count('reviews', distinct=True), Value(0), output_field=IntegerField()),
                effective_price=Coalesce(
                    Min('sales__sale__sale_price', filter=Q(sales__sale__is_active=True)),
                    F('price'),
                ),
            ).filter(filters, count__gte=1).distinct().select_related(
                'category'
                ).prefetch_related(
                    'images',
                    'tags',
                    'sales__sale',
                    )
        sort_by = ProductFilterService.get_sort_params(request.GET)
        return products.order_by(sort_by)

    def _paginate_products(self, request, products):
        """
        Пагинация продуктов.

        Attributes:
            request: Метаданные запроса.
            products: Список продуктов.
        """
        logger.debug('Product pagination.')
        page = int(request.GET.get('currentPage', self.DEFAULT_PAGE))
        limit = int(request.GET.get('limit', self.DEFAULT_LIMIT))

        paginator = Paginator(products, limit)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return {
            'items': page_obj.object_list,
            'current_page': page_obj.number,
            'last_page': paginator.num_pages,
            'total_count': paginator.count
        }

    def _build_response(self, data):
        """
        Построение ответа.

        Attributes:
            data: Данные ответа.
        """
        serializer = ProductSerializer(data['items'], many=True)
        logger.info('Construction of the answer.')
        return Response({
            'items': serializer.data,
            'currentPage': data['current_page'],
            'lastPage': data['last_page'],
        }, status=status.HTTP_200_OK)


class ProductDetailsView(APIView, BaseView):
    """
    Предствление работы с детальной информацией продукта.

    Methods:
        get(request, id)
            Основной метод получения продукта по ID.

        _get_product(request, id)
            Вспомогательный метод получения продукта по ID.

        _build_response(data)
            Метод построение ответа.

        _handle_error(message, error, status)
            Метод ответа ошибки.
    """
    def get(self, request, id:int):
        """
        GET /product/<int:id>

        Метод получения продукта по ID.

        Attributes:
            id(int): ID продукта.
        """
        try:
            logger.info('Get product with id: %s', id)
            product = self._get_product(id=id)
            return self._build_response(
                data=product,
                serializer=ProductDetailSerializer,
                status=status.HTTP_200_OK,
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
        Получение продуктов по ID.

        Attributes:
            id(int): Id продукта.
        """
        return Product.objects.select_related('category').prefetch_related(
                    'tags',
                    'specifications_values__specification',
                    'reviews',
                    'images',
                    'sales__sale',
                ).annotate(
                effective_price=Coalesce(
                    Min('sales__sale__sale_price', filter=Q(sales__sale__is_active=True)),
                    F('price'),
                )
            ).get(pk=id, count__gte=1)


class ProductPopularView(APIView, BaseView):
    """
    Представление работы с популярными продуктами.

    CONSTS:
        POPULAR_PRODUCTS_LIMIT: Лимит популярных продуктов.

    Methods:
        get(request)
            Основной метод получения популярных продуктов.

        _get_popular_products(request)
            Вспомогательный метод получения популярных продуктов.

        _build_response(data)
            Метод построение ответа.

        _handle_error(message, error, status)
            Метод ответа ошибки.
    """

    POPULAR_PRODUCTS_LIMIT = 8

    def get(self, request):
        """
        GET /products/popular

        Метод получения популярных продуктов.

        Attributes:
            request: Метаданные запроса.
        """
        try:
            logger.info('Get popular products.')
            products = self._get_popular_products()
            return self._build_response(
                data=products,
                serializer=ProductSerializer,
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

    def _get_popular_products(self):
        """
        Получение популярных продуктов.
        """
        logger.debug('Get popular products.')
        return Product.objects.filter(
            shopping_counter__gt=0,
            count__gte=1,
        ).select_related(
            'category',
                ).prefetch_related(
                    'tags',
                    'images',
                    'sales__sale',
                    ).annotate(
                        effective_price=Coalesce(
                            Min(
                                'sales__sale__sale_price',
                                filter=Q(sales__sale__is_active=True)
                                ),
                                F('price'),
                                )
                                ).order_by('-shopping_counter')[:self.POPULAR_PRODUCTS_LIMIT]


class ProductLimitedView(APIView, BaseView):
    """
    Представление работы с продуктами.

    Methods:
        get(request)
            Основной метод получения продуктов с ограниченным тиражом.

        _get_limited_products(request)
            Вспомогательный метод получения продуктов с ограниченным тиражом.

        _build_response(data)
            Метод построение ответа.

        _handle_error(message, error, status)
            Метод ответа ошибки.
    """
    def get(self, request):
        """
        GET /products/limited

        Метод получения продуктов с ограниченным тиражом.
        """
        try:
            logger.info('Get limited products.')
            products = self._get_limited_products()
            return self._build_response(
                data=products,
                serializer=ProductSerializer,
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

    def _get_limited_products(self):
        """
        Получения продуктов с ограниченным тиражом.
        """
        logger.debug('Get limited products.')
        return Product.objects.filter(
            limited_edition=True,
            count__gte=1,
        ).select_related(
            'category',
            ).prefetch_related(
                'tags',
                'images',
                ).annotate(
                    effective_price=Coalesce(
                    Min('sales__sale__sale_price', filter=Q(sales__sale__is_active=True)),
                    F('price'),
                )
            )[:16]

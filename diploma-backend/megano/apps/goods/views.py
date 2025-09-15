from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count, Value, IntegerField
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import  Product
from .serializers import ProductDetailSerializer, ProductSerializer
from .utils.filter_and_sort_catalog import ProductFilterService


class ProductView(APIView):
    """
    Представление работы с каталогом.
    """
    def get(self, request):
        """
        GET /catalog

        Метод получения продуктов по фильтрам.
        """
        try:
            # Построение фильтров
            filters = ProductFilterService.build_filters(request.GET)
            # Аннотация и фильтрация продуктов
            products = Product.objects.annotate(
                reviews_count=Coalesce(Count('reviews'), Value(0), output_field=IntegerField())
            ).filter(filters).distinct()
            # Сортировка
            sort_by = ProductFilterService.get_sort_params(request.GET)
            products = products.order_by(sort_by)

            # Пагинация
            page = int(request.GET.get('currentPage', 1))
            limit = int(request.GET.get('limit', 20))

            # Создаем пагинатор
            paginator = Paginator(products, limit)

            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)

            # Сериализация
            serializer = ProductSerializer(page_obj.object_list, many=True)
            return Response({
                'items': serializer.data,
                'currentPage': page_obj.number,
                'lastPage': paginator.num_pages,
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response(
                {'error': 'The price must be a number.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )



class ProductDetailsView(APIView):
    """
    Предствление работы с детальной информацией продукта.
    """
    def get(self, request, id:int):
        """
        GET /product/<int:id>

        Метод получения продукта по ID.

        Attributes:
            id(int): ID продукта.
        """
        try:
            product = Product.objects.select_related('category').prefetch_related(
                    'tags',
                    'specifications_values__specification',
                    'reviews',
                    'images'
                ).get(pk=id)
            serializer = ProductDetailSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductPopularView(APIView):
    """
    Представление работы с популярными продуктами.
    """
    def get(self, request):
        """
        GET /products/popular

        Метод получения каталога ограниченных товаров.
        """
        try:
            product = Product.objects.filter(
            shopping_counter__gt=0
        ).order_by('-shopping_counter')[:8]
            serializer = ProductSerializer(product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductLimitedView(APIView):
    """
    Представление работы с продуктами.
    """
    def get(self, request):
        """
        GET /products/limited

        Метод получения каталога ограниченных продуктов.
        """
        try:
            product = Product.objects.filter(limited_edition=True)[:16]
            serializer = ProductSerializer(product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
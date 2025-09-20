from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count, Value, IntegerField
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.goods.models import Product
from .serializers import BannerSerializer


class BannerView(APIView):
    """
    Предствление работы с банером сайта.
    """
    def get(self, request):
        """
        GET /banners

        Метод получения банера.
        """
        try:
            product = Product.objects.select_related('category').prefetch_related(
                    'tags',
                    'specifications_values__specification',
                    'reviews',
                    'images'
                ).annotate(reviewsCount=Count('reviews'))[:5]
            serializer = BannerSerializer(product, many=True)
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import SaleProduct
from .serializers import SaleProductSerializer

class SalesView(APIView):
    """
    Представление работы с продуктами со скидкой.
    """
    def get(self, request):
        """
        GET /sales

        Метод получения продуктов со скидкой.
        """
        try:
            # Фильтруем продукты с ненулевой скидкой
            sale_products = SaleProduct.objects.select_related('product')
            # Пагинация
            page = int(request.GET.get('currentPage', 1))
            limit = int(request.GET.get('limit', 20))

            # Создаем пагинатор
            paginator = Paginator(sale_products, limit)
            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            serializer = SaleProductSerializer(page_obj.object_list, many=True)
            return Response({
                'items': serializer.data,
                'currentPage': page_obj.number,
                'lastPage': paginator.num_pages,
            }, status=status.HTTP_200_OK)

        except Exception:
            return Response(
                {"error": "Internal server error"},
                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,)

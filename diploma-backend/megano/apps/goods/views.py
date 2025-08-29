from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Product, Review
from .serializer import ProductDetailSerializer, ReviewCreateSerializer


class ProductDetailsView(APIView):
    """
    Получение продукта.
    """
    def get(self, request, id: int):
        try:
            product = Product.objects.select_related('category').prefetch_related(
                    'tags',
                    'specifications_values__specification',
                    'reviews__author',
                    'images'
                ).get(pk=id)

        except Product.DoesNotExist:
            return Response(
                {"error": f"Продукт с ID {id} не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        # Проверяем существование продукта
        try:
            Product.objects.get(pk=id)

            # Проверяем, не оставлял ли пользователь уже отзыв
            if Review.objects.filter(product_id=id, author=request.user).exists():
                return Response(
                    {"error": "Вы уже оставили отзыв на этот продукт"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            data = request.data.copy()
            data['product'] = id
            data['author'] = request.user.id

            serializer = ReviewCreateSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "product_id": id,
                    "review_id": serializer.instance.id
                }, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

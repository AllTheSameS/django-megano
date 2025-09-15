from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.goods.models import Product

from .serializers import ReviewCreateSerializer
from .models import Review


class ReviewView(APIView):
    """
    Представление работы с отзывами продукта.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        """
        POST /product/<int:id>/reviews

        Метод создания отзыва о продукте по ID.

        Attributes:
            id(int): ID продукта.
        """
        try:
            product = Product.objects.get(pk=id)
            if product.reviews.filter(author=request.user).exists():
                return Response(
                        {"error": "You have already left a review for this product."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            request.data['product'] = id
            request.data['author'] = request.user.id
            serializer = ReviewCreateSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_product_rating(self):
        """Обновление рейтинга продукта на основе всех отзывов"""
        product_reviews = Review.objects.filter(
            product__product=self.product
        )

        if product_reviews.exists():
            # Вычисляем средний рейтинг
            total_rating = sum(review.rate for review in product_reviews)
            average_rating = total_rating / product_reviews.count()

            # Округляем до 2 знаков после запятой
            self.product.rating = round(average_rating, 2)
            self.product.save()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Product, Review, Tag
from .serializer import ProductDetailSerializer, ReviewCreateSerializer, GetTagsSerializer


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
                    'reviews__author',
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


class ProductReviewView(APIView):
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
            Product.objects.get(pk=id)

            if Review.objects.filter(product_id=id, author=request.user).exists():
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


class TagsView(APIView):
    """
    Представление рыботы с тэгами.
    """
    def get(self, request):
        """
        GET /tags

        Метод получения всех тэгов.
        """
        try:
            tags = Tag.objects.all()
            serializer = GetTagsSerializer(tags, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

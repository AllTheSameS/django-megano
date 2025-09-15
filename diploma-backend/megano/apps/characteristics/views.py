from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Tag, Category
from .serializers import GetTagsSerializer, CategorySerializer


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


class CategoriesView(APIView):
    """
    Представление работы с категориями.
    """
    def get(self, request):
        """
        GET /categories

        Метод получения всех категорий.
        """
        try:
            categories = Category.objects.filter(
                parent__isnull=True,
                )
            serializer = CategorySerializer(categories, many=True,)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
                )
        except Exception:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

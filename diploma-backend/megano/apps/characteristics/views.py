"""
Модуль представлений приложения "characteristics".

Views:
    TagsView()
        Представление рыботы с тэгами.

    CategoriesView()
        Представление работы с категориями.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Tag, Category
from .serializers import GetTagsSerializer, CategorySerializer

from apps.utils.utils import BaseView

import logging

logger = logging.getLogger('characteristics')


class TagsView(APIView, BaseView):
    """
    Представление рыботы с тэгами.

    Methods:
        get: Метод получения всех тэгов.
        _get_all_tags: Вспомогательный метод получения всех тэгов.
    """
    def get(self, request):
        """
        GET /tags

        Метод получения всех тэгов.
        """
        try:
            logger.info('Get all tags.')
            tags = self._get_all_tags()
            return self._build_response(
                data=tags,
                serializer=GetTagsSerializer,
                status=status.HTTP_200_OK,
                logger=logger,
                many=True,
            )
        except Exception:
            return self._handle_error(
                message='Internal server error.',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )

    def _get_all_tags(self):
        """
        Вспомогательный метод получения всех тэгов.
        """
        return Tag.objects.all()

class CategoriesView(APIView, BaseView):
    """
    Представление работы с категориями.

    Methods:
        get: Метод получение всех категорий.
        _get_all_categories: Вспомогательный метод получения всех категорий.
    """
    def get(self, request):
        """
        GET /categories

        Метод получения всех категорий.
        """
        try:
            categories = self._get_all_categories()
            return self._build_response(
                data=categories,
                serializer=CategorySerializer,
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

    def _get_all_categories(self):
        """
        Вспомогательный метод получения всех категорий.
        """
        return Category.objects.filter(parent__isnull=True,)

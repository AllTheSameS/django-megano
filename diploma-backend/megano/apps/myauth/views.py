"""
Модуль представлений приложения "myauth".

Views:
    SignInView()
        Представление аутентификации пользователя.

    SignUpView()
        Предствление регистрации пользователя.

    ProductPopularView()
        Представление работы с популярными продуктами.

    ProductLimitedView()
        Представление работы с продуктами.
"""

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser

from .models import Profile, Avatar
from .serializers import ProfileSerializer, AvatarUpdateSerializer

from apps.utils.utils import BaseView

import json
import uuid
import logging

logger = logging.getLogger('myauth')


class SignInView(APIView, BaseView):
    """
    Представление аутентификации пользователя.

    Methods:
        post: Аутентификация пользователя.
    """
    def post(self, request):
        """
        Аутентификация пользователя.

        POST /api/sign-in

        Attributes:
            request: Метаданные запроса.
        """
        try:
            serialized_data = json.loads(request.body)
            username = serialized_data["username"]
            password = serialized_data["password"]
            logger.info('User authentication %s', username)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return self._build_response(
                    status=status.HTTP_200_OK,
                    logger=logger,
                )
            else:
                return self._handle_error(
                    message='Authentication Error.',
                    status=status.HTTP_400_BAD_REQUEST,
                    logger=logger,
                    )
        except Exception as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )


class SignUpView(APIView, BaseView):
    """
    Предствление регистрации пользователя.

    Methods:
        post: Регистрация пользователя.
    """
    def post(self, request):
        """
        Регистрация пользователя.

        POST /api/sign-up

        Attributes:
            request: Метаданные запроса.
        """
        serialized_data = json.loads(request.body)
        name = serialized_data["name"]
        username = serialized_data["username"]
        password = serialized_data["password"]

        logger.info('User registration %s', username)
        try:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user, full_name=name)
            Avatar.objects.create(profile=profile)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            return self._build_response(
                status=status.HTTP_201_CREATED,
                logger=logger,
            )
        except Exception as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )


class SignOut(APIView, BaseView):
    """
    Представление выхода пользователя.
    """

    def post(self, request):
        """
        Выход пользователя.

        POST /api/sign-out

        Attributes:
            request: Метаданные запроса.

        """
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ProfileView(APIView, BaseView):
    """
    Предствление работы с профилем пользователя.

    Methods:
        get: Получение профиля пользователя.
        post: Создание профиля пользователя.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Получение профиля пользователя.

        GET /api/profile

        Attributes:
            request: Метаданные запроса.
        """
        try:
            profile = Profile.objects.get(user=request.user)
            return self._build_response(
                data=profile,
                serializer=ProfileSerializer,
                status=status.HTTP_200_OK,
                logger=logger,
            )
        except Exception as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )

    def post(self, request):
        """
        Создание профиля пользователя.

        POST /api/profile

        Attributes:
            request: Метаданные запроса.
        """
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return self._handle_error(
                    message=str(serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST,
                    logger=logger,
                )
        except Exception as e:
            return self._handle_error(
                    message=str(e),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    logger=logger,
                )


class ProfileUpdatePasswordView(APIView, BaseView):
    """
    Обновление профиля пользователя.

    Methods:
        post: Обновление профиля пользователя.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Обновление профиля пользователя.

        POST /api/profile/password

        Attributes:
            request: Метаданные запроса.
        """
        user = request.user

        old_password = request.data.get("currentPassword")
        new_password = request.data.get("newPassword")

        if not all([old_password, new_password]):
            return self._handle_error(
                message='All fields are required.',
                status=status.HTTP_400_BAD_REQUEST,
                logger=logger,
            )

        if not check_password(old_password, user.password):
            return self._handle_error(
                message='Incorrect current password.',
                status=status.HTTP_400_BAD_REQUEST,
                logger=logger,
            )

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        return Response(
            {"success": "Password changed successfully."},
            status=status.HTTP_200_OK
        )


class ProfileUpdateAvatar(APIView, BaseView):
    """
    Обновление аватара профиля.

    Methods:
        post: Метод обновление аватара профиля.
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        """
        Метод обновление аватара профиля.

        Attributes:
            request: Метаданные запроса.
        """
        try:
            profile = request.user.profile
            avatar_file = request.FILES["avatar"]
            avatar_file.name = uuid.uuid4().hex + avatar_file.name
            serializer = AvatarUpdateSerializer(
                profile.avatar,
                data={'src': avatar_file},
                partial=True,
                )
            if serializer.is_valid():
                serializer.save()
            return Response(
                status=status.HTTP_200_OK
            )
        except Exception:
            return self._handle_error(
                message='Internal server error.',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )

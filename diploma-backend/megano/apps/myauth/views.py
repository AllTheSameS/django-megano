from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import Profile
from .logging import get_logger

import json


logger = get_logger(__name__)


class SignInView(APIView):
    """
    API для аутентификации пользователя.

    Обработка POST-запроса на вход пользователя в систему,
    проверяет учётные данные и возвращает соответствующие токены JWT или сообщения об ошибках.

    Attributes:
        permission_classes (list): Доступ без аутентификации
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            if not request.data:
                return Response(
                    {"error": "Need to pass data to user"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                data = request.data if isinstance(request.data, dict) else json.loads(list(request.data.keys())[0])
            except (json.JSONDecodeError, AttributeError, IndexError):
                return Response(
                    {"error": "Invalid data format"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return Response(
                    {"error": "Username and password are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return Response(
                    {"message": "Login successful"},
                    status=status.HTTP_200_OK
                )

            logger.warning(f"Failed login attempt for username: {username}")
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except Exception as e:
            return Response(
                {"error": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SignUpView(APIView):
    """
    API для регистрации пользователя.

    Обработка POST-запроса на регистрацию пользователя в системе,
    проверяет учётные данные и возвращает соответствующие токены JWT или сообщения об ошибках.

    Attributes:
        permission_classes (list): Доступ без аутентификации
    """
    def post(self, request):
        try:
            if not request.data:
                return Response(
                    {"error": "Need to pass data to user"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                user_data = request.data if isinstance(request.data, dict) else json.loads(list(request.data.keys())[0])
            except (json.JSONDecodeError, AttributeError, IndexError):
                return Response(
                    {"error": "Invalid data format"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            required_fields = ['username', 'password', 'name']
            if not all(field in user_data for field in required_fields):
                return Response(
                    {"error": f"Required fields: {', '.join(required_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            username = user_data['username']
            password = user_data['password']
            name = user_data['name']

            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": "A user with this name already exists"},
                    status=status.HTTP_409_CONFLICT
                )

            try:
                user = User.objects.create_user(
                    username=username,
                    password=password
                )
                profile = Profile.objects.create(
                    user=user,
                    first_name=name
                )

                user = authenticate(
                    request,
                    username=username,
                    password=password
                )

                if user is not None:
                    login(request, user)
                    return Response(
                        {"success": "The user has been successfully registered and authorized."},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {"error": "Authentication Error"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            except Exception as e:
                if 'user' in locals():
                    user.delete()
                return Response(
                    {"error": f"Error creating user: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            return Response(
                {"error": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
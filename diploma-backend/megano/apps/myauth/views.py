from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser

from .models import Profile, Avatar
from .serializer import ProfileSerializer, AvatarUpdateSerializer
from .utils.delete_avatar import delete_avatar

import json
import uuid

class SignInView(APIView):
    def post(self, request):
        serialized_data = json.loads(request.body)
        username = serialized_data["username"]
        password = serialized_data["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    def post(self, request):
        serialized_data = json.loads(request.body)
        name = serialized_data["name"]
        username = serialized_data["username"]
        password = serialized_data["password"]

        try:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user, full_name=name)
            Avatar.objects.create(profile=profile)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            return Response(status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def signOut(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdatePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        old_password = request.data.get("currentPassword")
        new_password = request.data.get("newPassword")

        if not all([old_password, new_password]):
            return Response(
                {"error": "Все поля обязательны"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(old_password, user.password):
            return Response(
                {"error": "Неверный текущий пароль"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        return Response(
            {"success": "Пароль успешно изменен"},
            status=status.HTTP_200_OK
        )


class ProfileUpdateAvatar(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
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
            return Response(
                {"error": "Произошла ошибка при загрузке аватара"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

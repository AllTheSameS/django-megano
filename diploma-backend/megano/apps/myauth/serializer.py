from rest_framework import serializers
from megano.settings import DEFAULT_AVATAR_PATH

from .models import Avatar, Profile


class AvatarUpdateSerializer(serializers.ModelSerializer):
    src = serializers.ImageField(write_only=True)

    class Meta:
        model = Avatar
        fields = ["src", "alt"]
        extra_kwargs = {
            'alt': {'required': False}
        }

    def update(self, instance, validated_data):
        avatar_file = validated_data.pop('src', None)
        if avatar_file:
            if instance.src and instance.src != DEFAULT_AVATAR_PATH:
                instance.src.delete(save=False)
            instance.src = avatar_file
        return super().update(instance, validated_data)


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.ImageField(read_only=True)

    class Meta:
        model = Avatar
        fields = ["src", "alt"]
        extra_kwargs = {
            'alt': {'required': False}
        }


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(read_only=True)
    fullName = serializers.CharField(source='full_name', max_length=128)

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]

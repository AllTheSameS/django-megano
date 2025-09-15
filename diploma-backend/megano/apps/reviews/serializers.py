from rest_framework import serializers

from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Review
        fields = ['author', 'text', 'rate', 'date']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'text', 'rate', 'date', 'author']

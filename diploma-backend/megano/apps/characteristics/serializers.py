from rest_framework import serializers

from .models import Tag, Category, CategoryImage, ProductSpecification


class GetTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ['src', 'alt']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField(source='children')
    image = CategoryImageSerializer()
    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']

    def get_subcategories(self, obj):
        subcategory = obj.children.all()
        return CategorySerializer(subcategory, many=True).data


class SpecificationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='specification.name')
    value = serializers.CharField()

    class Meta:
        model = ProductSpecification
        fields = ['name', 'value']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name',]

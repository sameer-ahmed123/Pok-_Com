from rest_framework import serializers
from products.models import *


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'pokemon_id',
            'name',
            'image_url',
            'description',
            'price',
            'is_active'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

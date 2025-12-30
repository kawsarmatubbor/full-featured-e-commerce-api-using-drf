from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'description', 'icon']
        extra_kwargs = {
            'slug' :  {'required' : False},
            'description' : {'required' : False},
        }

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'category', 'image', 'price']
        extra_kwargs = {
            'slug' :  {'required' : False},
            'description' : {'required' : False},
        }
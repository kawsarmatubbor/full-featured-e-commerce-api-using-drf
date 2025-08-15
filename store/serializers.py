from rest_framework import serializers
from . import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'title', 'slug', 'description', 'is_active']
        extra_kwargs = {
            'description' : {'required' : False},
            'slug' :  {'required' : False}
        }

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'title', 'slug', 'description', 'category', 'image', 'price', 'is_active']
        extra_kwargs = {
            'description' : {'required' : False},
            'slug' :  {'required' : False},
            'image': {'required': False}
        }

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartProducts
        fields = ['id', 'product', 'quantity', 'subtotal', 'is_active']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id', 'address', 'order_date', 'is_active']

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderProducts
        fields = ['id', 'order', 'product', 'quantity', 'subtotal', 'is_active']
        extra_kwargs = {
            'order' : {'write_only' : True}
        }
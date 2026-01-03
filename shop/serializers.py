from rest_framework import serializers
from .models import Category, Product, Cart, CartProduct

# Category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'description', 'icon']
        extra_kwargs = {
            'slug' :  {'required' : False},
            'description' : {'required' : False},
        }

# Product serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'category', 'image', 'price']
        extra_kwargs = {
            'slug' :  {'required' : False},
            'description' : {'required' : False},
        }

# Cart serializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user']
        extra_kwargs = {
            'user' : {'read_only' : True}
        }

# Cart product serializer
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['id', 'cart', 'product', 'quantity', 'sub_total']
        extra_kwargs = {
            'cart' : {'read_only' : True}
        }
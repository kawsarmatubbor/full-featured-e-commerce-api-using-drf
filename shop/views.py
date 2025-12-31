from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, Cart
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    CartSerializer
)
from .permission import IsAdminOrReadOnly

# Category view
class CategoriesViewSet(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        categories = Category.objects.filter(is_active = True)
        serializers = CategorySerializer(categories, many = True)
        return Response(serializers.data)
    
    def post(self, request):
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": "Category created successful.",
                "category": serializer.data
            })
        return Response(serializer.errors)

# Category details view   
class CategoryDetailsViewSet(APIView):
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug, is_active=True)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        
        except Category.DoesNotExist:
            return Response({
                "error": "Category does not exist."
            })
    
    def put(self, request, slug):
        try:
            category = Category.objects.get(slug=slug, is_active=True)
            serializer = CategorySerializer(category, data = request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": "Category updated successful.",
                    "category": serializer.data
                })
            return Response(serializer.errors)
        
        except Category.DoesNotExist:
            return Response({
                "error": "Category does not exist."
            })

    def delete(self, request, slug):
        try:
            category = Category.objects.get(slug=slug, is_active=True)
            category.delete()
            return Response({
                "success": "Category deleted successful."
            })
        
        except Category.DoesNotExist:
            return Response({
                "error": "Category does not exist."
            })
        
# Product view
class ProductViewSet(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        products = Product.objects.filter(is_active = True)
        serializers = ProductSerializer(products, many = True)
        return Response(serializers.data)
    
    def post(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": "Product created successful.",
                "category": serializer.data
            })
        return Response(serializer.errors)
    
# Product details view
class ProductDetailsViewSet(APIView):
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug, is_active=True)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        
        except Product.DoesNotExist:
            return Response({
                "error": "Product does not exist."
            })
    
    def put(self, request, slug):
        try:
            product = Product.objects.get(slug=slug, is_active=True)
            serializer = ProductSerializer(product, data = request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": "Product updated successful.",
                    "product": serializer.data
                })
            return Response(serializer.errors)
        
        except Product.DoesNotExist:
            return Response({
                "error": "Product does not exist."
            })

    def delete(self, request, slug):
        try:
            product = Product.objects.get(slug=slug, is_active=True)
            product.delete()
            return Response({
                "success": "Product deleted successful."
            })
        
        except Product.DoesNotExist:
            return Response({
                "error": "Product does not exist."
            })
        
# Cart view
class CartViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user = request.user, is_active = True)
        serializers = CartSerializer(cart_items, many = True)
        return Response(serializers.data)
    
    def post(self, request):
        serializer = CartSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response({
                "success": "Product add to cart successful.",
                "cart": serializer.data
            })
        return Response(serializer.errors)
    
# Cart item details view
class CartItemDetailsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            cart_item = Cart.objects.get(id=id, user=request.user, is_active=True)
            serializer = CartSerializer(cart_item, data = request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": "Cart updated successful.",
                    "cart_item": serializer.data
                })
            return Response(serializer.errors)
        
        except Cart.DoesNotExist:
            return Response({
                "error": "Cart item does not exist."
            })

    def delete(self, request, id):
        try:
            cart_item = Cart.objects.get(id=id, user=request.user, is_active=True)
            cart_item.delete()
            return Response({
                "success": "Cart item deleted successful."
            })
        
        except Cart.DoesNotExist:
            return Response({
                "error": "Cart item does not exist."
            })
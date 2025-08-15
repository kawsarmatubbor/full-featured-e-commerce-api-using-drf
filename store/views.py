from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from . import permissions

class CategoriesViewSet(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    def get(self, request):
        categories = models.Category.objects.filter(is_active = True)
        serializer = serializers.CategorySerializer(categories, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success" : "Category create successful."
            })
        return Response(serializer.errors)
    
class CategoryDetailViewSet(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            category = models.Category.objects.get(pk = pk)
            serializer = serializers.CategorySerializer(category)
            return Response(serializer.data)
        
        except models.Category.DoesNotExist:
            return Response({
                "error" : "Category not found."
            })
                
    def put(self, request, pk):
        try:
            category = models.Category.objects.get(pk = pk)
            serializer = serializers.CategorySerializer(category, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success" : "Product update successful."
                })
            return Response(serializer.errors)
        
        except models.Category.DoesNotExist:
            return Response({
                "error" : "Category not found."
            })
            
    def delete(self, request, pk):
        try:
            category = models.Category.objects.get(pk = pk)
            category.delete()
            return Response({
                "success" : "Category delete successful."
            })
        
        except models.Product.DoesNotExist:
            return Response({
                "error" : "Category not found."
            })
        
class ProductsViewSet(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    def get(self, request):
        products = models.Product.objects.filter(is_active = True)
        serializer = serializers.ProductSerializer(products, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success" : "Product create successful."
            })
        return Response(serializer.errors)
        
class ProductDetailViewSet(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            product = models.Product.objects.get(pk = pk)
            serializer = serializers.ProductSerializer(product)
            return Response(serializer.data)
        
        except models.Product.DoesNotExist:
            return Response({
                "error" : "Product not found."
            })
                
    def put(self, request, pk):
        try:
            product = models.Product.objects.get(pk = pk)
            serializer = serializers.ProductSerializer(product, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success" : "Product update successful."
                })
            return Response(serializer.errors)
        
        except models.Product.DoesNotExist:
            return Response({
                "error" : "Product not found."
            })
            
    def delete(self, request, pk):
        try:
            product = models.Product.objects.get(pk = pk)
            product.delete()
            return Response({
                "success" : "Product delete successful."
            })
        
        except models.Product.DoesNotExist:
            return Response({
                "error" : "Product not found."
            })
        
class CartProductViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cart_products = models.CartProducts.objects.filter(user = request.user)
        serializer = serializers.CartProductSerializer(cart_products, many = True)
        return Response(serializer.data)

        
    def post(self, request):
            serializer = serializers.CartProductSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(user = request.user)
                return Response({
                    "message" : "Product added to cart successfully."
                })
            return Response(serializer.errors)
    
class CartProductDetailViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            cart_product = models.CartProducts.objects.get(pk = pk)
            serializer = serializers.CartProductSerializer(cart_product)
            return Response(serializer.data)
        except models.CartProducts.DoesNotExist:
            return Response({
                "error" : "Product not found."
            })
    
    def put(self, request, pk):
        try:
            cart_product = models.CartProducts.objects.get(pk = pk)
            serializer = serializers.CartProductSerializer(cart_product, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success" : "Cart update successful."
                })
            return Response(serializer.data)
        except models.CartProducts.DoesNotExist:
            return Response({
                "error" : "Product not found."
            })
        
    def delete(self, request, pk):
        try:
            cart_product = models.CartProducts.objects.get(pk = pk)
            cart_product.delete()
            return Response({
                "success" : "Product delete successful"
            })
        except models.CartProducts.DoesNotExist:
            return Response({
                "error" : "Product not found."
            })
        
class OrderViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = models.Order.objects.filter(user = request.user)
        serializer = serializers.OrderSerializer(orders, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.OrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response("Order created successful.")
        return Response(serializer.errors)
    
class OrderProductViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = models.Order.objects.filter(user = request.user)
        order_products = models.OrderProducts.objects.filter(order__in = orders)
        if not order_products:
            return Response({
                "error" : "Order does not exist."
            })
        serializer = serializers.OrderProductSerializer(order_products, many = True)
        return Response(serializer.data)

    def post(self, request):
            serializer = serializers.OrderProductSerializer(data = request.data)
            if serializer.is_valid():
                order = serializer.validated_data.get('order')
                print("Received order:", order.user)
                serializer.save()
                return Response({
                    "message" : "Product added to order successfully."
                })
            return Response(serializer.errors)
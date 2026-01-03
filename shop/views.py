from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, Cart, CartProduct, Order, OrderProduct
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    CartSerializer,
    CartProductSerializer,
    OrderSerializer,
    OrderProductSerializer
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
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active = True)
        cart_products = CartProduct.objects.filter(cart = cart, is_active = True)
        serializer = CartProductSerializer(cart_products, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(cart = cart)
            return Response({
                "success": "Product add to cart successful.",
                "cart": serializer.data
            })
        return Response(serializer.errors)

# Cart product details view
class CartProductDetailsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            cart = Cart.objects.get(user = request.user, is_active = True)
            cart_product = CartProduct.objects.get(id = id, cart = cart, is_active = True)
            serializer = CartProductSerializer(cart_product)
            return Response(serializer.data)
        
        except CartProduct.DoesNotExist:
            return Response({
                "error": "Cart product does not exist."
            })
    
    def put(self, request, id):
        try:
            cart = Cart.objects.get(user = request.user, is_active = True)
            cart_product = CartProduct.objects.get(id = id, cart = cart, is_active = True)
            serializer = CartProductSerializer(cart_product, data = request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": "Cart updated successful.",
                    "cart_item": serializer.data
                })
            return Response(serializer.errors)
        
        except CartProduct.DoesNotExist:
            return Response({
                "error": "Cart product does not exist."
            })
        
    def delete(self, request, id):
        try:
            cart = Cart.objects.get(user = request.user, is_active = True)
            cart_product = CartProduct.objects.get(id = id, cart = cart, is_active = True)
            cart_product.delete()
            return Response({
                "success": "Cart product deleted successful."
            })
        
        except CartProduct.DoesNotExist:
            return Response({
                "error": "Cart product does not exist."
            })

# Checkout view
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart = Cart.objects.get(user = request.user, is_active = True)
            cart_products = CartProduct.objects.filter(cart = cart, is_active = True)

            if not cart_products.exists():
                return Response({
                    "error": "Cart is empty."
                })
            
            tracking_id = get_random_string(length=12).upper()

            total_price = 0
            for cart_product in cart_products:
                total_price += cart_product.sub_total

            order_serializer = OrderSerializer(data = request.data)
            if order_serializer.is_valid():
                order = order_serializer.save(
                    user = request.user,
                    tracking_id = tracking_id,
                    total_price = total_price,
                )

                for cart_product in cart_products:
                    OrderProduct.objects.create(
                        order = order,
                        product = cart_product.product,
                        price = cart_product.product.price,
                        quantity = cart_product.quantity,
                    )
                    

                cart.is_active = False
                cart.save()
                for cart_product in cart_products:
                    cart_product.is_active = False
                    cart_product.save()

                return Response({
                    "success" : "Order placed successful.",
                    "order": order_serializer.data
                })
            return Response(order_serializer.errors)
            
        except Cart.DoesNotExist:
            return Response({
                "error": "No cart found."
            })
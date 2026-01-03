from django.urls import path
from .views import (
    CategoriesViewSet, 
    CategoryDetailsViewSet, 
    ProductViewSet, 
    ProductDetailsViewSet,
    CartViewSet,
    CartProductDetailsViewSet,
    CheckoutView
)

urlpatterns = [
    path('categories/', CategoriesViewSet.as_view(), name='categories'),
    path('categories/<slug:slug>', CategoryDetailsViewSet.as_view(), name='category_details'),
    path('products/', ProductViewSet.as_view(), name='products'),
    path('products/<slug:slug>', ProductDetailsViewSet.as_view(), name='product_details'),
    path('cart/', CartViewSet.as_view(), name='cart'),
    path('cart-products/<int:id>', CartProductDetailsViewSet.as_view(), name='cart_product_details'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]

from django.urls import path
from .views import (
    CategoriesViewSet, 
    CategoryDetailsViewSet, 
    ProductViewSet, 
    ProductDetailsViewSet,
    CartViewSet,
    CartItemDetailsViewSet,
)

urlpatterns = [
    path('categories/', CategoriesViewSet.as_view(), name='categories'),
    path('categories/<slug:slug>', CategoryDetailsViewSet.as_view(), name='category_details'),
    path('products/', ProductViewSet.as_view(), name='products'),
    path('products/<slug:slug>', ProductDetailsViewSet.as_view(), name='products_details'),
    path('cart/', CartViewSet.as_view(), name='cart'),
    path('cart/<int:id>', CartItemDetailsViewSet.as_view(), name='cart_item'),
]

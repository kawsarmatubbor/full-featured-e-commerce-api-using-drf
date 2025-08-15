from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoriesViewSet.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetailViewSet.as_view(), name='category-detail'),
    path('products/', views.ProductsViewSet.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetailViewSet.as_view(), name='product-detail'),
    path('cart-products/', views.CartProductViewSet.as_view(), name='cart-products'),
    path('cart-products/<int:pk>/', views.ProductDetailViewSet.as_view(), name='cart-product-detail'),
    path('orders/', views.OrderViewSet.as_view(), name='orders'),
    path('order-products/', views.OrderProductViewSet.as_view(), name='order-products'),
]

from django.urls import path
from .views import CategoriesViewSet, CategoryDetailsViewSet, ProductViewSet, ProductDetailsViewSet

urlpatterns = [
    path('categories/', CategoriesViewSet.as_view(), name='categories'),
    path('categories/<slug:slug>', CategoryDetailsViewSet.as_view(), name='category_details'),
    path('products/', ProductViewSet.as_view(), name='products'),
    path('products/<slug:slug>', ProductDetailsViewSet.as_view(), name='products_details'),
]

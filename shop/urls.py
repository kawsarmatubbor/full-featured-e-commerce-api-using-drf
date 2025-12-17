from django.urls import path
from .views import CategoriesViewSet, CategoryDetailsViewSet

urlpatterns = [
    path('categories/', CategoriesViewSet.as_view(), name='categories'),
    path('categories/<slug:slug>', CategoryDetailsViewSet.as_view(), name='category_details'),
]

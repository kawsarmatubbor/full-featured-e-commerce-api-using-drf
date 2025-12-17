from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer
from .permission import IsAdminOrReadOnly

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
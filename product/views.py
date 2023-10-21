from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated, AllowAny, IsAdminUser)
from rest_framework.decorators import action

from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_class = IsAuthenticated
    queryset = Product.objects.all()
    lookup_field = "pk"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.all()
        elif self.action == "product_images":
            queryset = ProductImage.objects.all()
        return queryset
    
    def get_object(self):
        obj = super().get_object()
        if self.action == "product_images":
            obj = ProductImage
        return obj

    def get_serializer_class(self):
        if self.action == "product_images":
            self.serializer_class = ProductImageSerializer
        return super().get_serializer_class()
    
    @action(["get", "put", "patch", "delete", "post"], detail=True)
    def product_images(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)
        elif request.method == "POST":
            return self.create(request, *args, **kwargs)
    

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = "pk"

    def get_permissions(self):
        if self.action == "get":
            self.permission_classes = [AllowAny]
        elif self.action == "list":
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    

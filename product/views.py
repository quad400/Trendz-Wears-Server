from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated, AllowAny, IsAdminUser)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework import status,views, pagination, filters

from .models import Product, ProductImage, ProductSizes, ProductColor
from .serializers import ProductSerializer, ProductImageSerializer, ProductColorSerializer, ProductSizeSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ]
    queryset = Product.objects.all()
    lookup_field = "pk"
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'desc']

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

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [AllowAny,]
        elif self.action == "retrieve":
            self.permission_classes = [AllowAny,]
        elif self.action == "product_images":

            self.permission_classes = [AllowAny, ]

        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ProductImageListCreateAPIView(views.APIView):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
    permission_classes = [IsAdminUser, ]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        id = kwargs["pk"]
        if Product.objects.filter(id=id).exists():

            serializer = ProductImageSerializer(data=request.data)
            if serializer.is_valid():
                image = serializer.validated_data.pop("image")
                serializer.save(image_product_id=id, image=image)
                return Response({"message": "Successfully created product image"}, status=status.HTTP_201_CREATED)
            return Response({"message": "Invalid Product image data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        id = kwargs["pk"]
        product_images = ProductImage.objects.filter(image_product_id=id)
        if product_images.exists():

            serializer = ProductImageSerializer(instance=product_images, many=True)
            print(self.request.method)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)

    
class ProductImageRetrieveDestroyAPIView(views.APIView):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
    permission_classes = [IsAdminUser, ]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()
    
    def get(self, request, *args, **kwargs):
        id = kwargs["pk"]
        product_images = ProductImage.objects.filter(id=id)
        if product_images.exists():

            serializer = ProductImageSerializer(instance=product_images[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Product Image does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        id = kwargs["pk"]
        product_images = ProductImage.objects.filter(id=id)
        if product_images.exists():
            product_images[0].delete()
            return Response({"message": "Successfully deleted this image"}, status=status.HTTP_200_OK)
        return Response({"message": "Product Image does not exist"}, status=status.HTTP_404_NOT_FOUND)
        

class ProductColorListCreateAPIView(views.APIView):
    permission_classes = [IsAdminUser, ]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        id = kwargs["pk"]
        if Product.objects.filter(id=id).exists():

            serializer = ProductColorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(color_product_id=id)
                return Response({"message": "Successfully created product color"}, status=status.HTTP_201_CREATED)
            return Response({"message": "Invalid Product color data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        id = kwargs["pk"]
        product_colors = ProductColor.objects.filter(color_product_id=id)
        if product_colors.exists():

            serializer = ProductColorSerializer(instance=product_colors, many=True)
            print(self.request.method)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)

    
class ProductColorRetrieveDestroyAPIView(views.APIView):
    permission_classes = [IsAdminUser, ]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()
    
    def get(self, request, *args, **kwargs):
        id = kwargs["pk"]
        product_colors = ProductColor.objects.filter(id=id)
        if product_colors.exists():

            serializer = ProductColorSerializer(instance=product_colors[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Product color does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        id = kwargs["pk"]
        product_images = ProductColor.objects.filter(id=id)
        if product_images.exists():
            product_images[0].delete()
            return Response({"message": "Successfully deleted this color"}, status=status.HTTP_200_OK)
        return Response({"message": "Product color does not exist"}, status=status.HTTP_404_NOT_FOUND)
        

class ProductSizeListCreateAPIView(views.APIView):
    permission_classes = [IsAdminUser, ]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        id = kwargs["pk"]
        if Product.objects.filter(id=id).exists():

            serializer = ProductSizeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(size_product_id=id)
                return Response({"message": "Successfully created product Size"}, status=status.HTTP_201_CREATED)
            return Response({"message": "Invalid Product Size data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)


    def get(self, request, *args, **kwargs):
        id = kwargs["pk"]
        product_sizes = ProductSizes.objects.filter(size_product_id=id)
        if product_sizes.exists():

            serializer = ProductSizeSerializer(instance=product_sizes, many=True)
            print(self.request.method)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)

    
class ProductSizeRetrieveDestroyAPIView(views.APIView):
    permission_classes = [IsAdminUser, ]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()
    
    def get(self, request, *args, **kwargs):
        id = kwargs["pk"]
        product_sizes = ProductSizes.objects.filter(id=id)
        if product_sizes.exists():

            serializer = ProductSizeSerializer(instance=product_sizes[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Product Size does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        id = kwargs["pk"]
        product_sizes = ProductSizes.objects.filter(id=id)
        if product_sizes.exists():
            product_sizes[0].delete()
            return Response({"message": "Successfully deleted this size"}, status=status.HTTP_200_OK)
        return Response({"message": "Product Size does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
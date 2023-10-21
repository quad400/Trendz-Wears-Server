from django.urls import path

from .views import (ProductImageListCreateAPIView, 
                    ProductImageRetrieveDestroyAPIView,
                    ProductColorListCreateAPIView,
                    ProductColorRetrieveDestroyAPIView, 
                    ProductSizeListCreateAPIView,
                    ProductSizeRetrieveDestroyAPIView
                    )
urlpatterns = [
    path("<slug:pk>/images/", ProductImageListCreateAPIView.as_view(), name="product_images"),
    path("images/<slug:pk>/", ProductImageRetrieveDestroyAPIView.as_view(), name="product_images_id"),
    path("<slug:pk>/colors/", ProductColorListCreateAPIView.as_view(), name="product_color"),
    path("colors/<slug:pk>/", ProductColorRetrieveDestroyAPIView.as_view(), name="product_color_id"),
    path("<slug:pk>/sizes/", ProductSizeListCreateAPIView.as_view(), name="product_size"),
    path("sizes/<slug:pk>/", ProductSizeRetrieveDestroyAPIView.as_view(), name="product_size_id"),
]
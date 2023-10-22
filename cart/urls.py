from django.urls import path

from .views import CartAPIView, remove_product_from_cart

urlpatterns = [
    path("<slug:pk>/", CartAPIView.as_view(), name="cart"),
    path("remove/<slug:pk>/", remove_product_from_cart, name="remove_cart")
]
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication.views import UserViewSet
from product.views import ProductViewSet

router = DefaultRouter()
router.register("api/auth/users", UserViewSet)
router.register("api/product", ProductViewSet)

urlpatterns = [
    path('api/auth/users/', include('authentication.urls')),
    path('api/product/', include('product.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls

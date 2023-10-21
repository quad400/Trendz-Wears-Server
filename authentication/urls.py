from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView


urlpatterns = [
    # path("login/", TokenObtainPairView.as_view(), name="login"),
    path("verify/", TokenVerifyView.as_view(), name="verify"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
]


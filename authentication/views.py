import requests
import jwt
import random
from datetime import timedelta, datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from django.utils import timezone
from django.contrib.auth import logout, authenticate
from django.dispatch import Signal

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token


from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import (
    UserCreateSerializer,TokenSerializer,
    OTPSerializer, UserSerializer,
    LoginSerializer)
from core.permissions import CurrentUserOrAdmin, CurrentUserOrAdminOrReadOnly
from .email import ActivationEmail,ResendCodeEmail
from .tokens import create_jwt_pair_for_user


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_class = permissions.AllowAny
    lookup_field = "pk"

    def permission_denied(self, request, **kwargs):
        if (
            settings.HIDE_USERS
            and request.user.is_authenticated
            and self.action in ["update", "partial_update", "list", "retrieve"]
        ):
            raise NotFound()
        super().permission_denied(request, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.pk)
        return queryset

    def get_permissions(self):
        if self.action == "create":
            self.permission_class = permissions.AllowAny
        elif self.action == "activation":
            self.permission_class = permissions.AllowAny
        elif self.action == "resend_activation":
            self.permission_class = permissions.AllowAny
        elif self.action == "list":
            self.permission_class = CurrentUserOrAdmin
        elif self.action == "verify_otp":
            self.permission_class = permissions.AllowAny
        elif self.action == "destroy" or (self.action == "me" and self.request and self.request.method == "DELETE"):
            self.permission_class = CurrentUserOrAdmin
        
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "me":
            return UserSerializer
        elif self.action == "verify_otp":
            return OTPSerializer
        elif self.action == "login":
            return LoginSerializer
        return super().get_serializer_class()

    def get_instance(self):
        return self.request.user
    
    def perform_create(self, serializer, *args, **kwargs):
        # try:
            user = serializer.save(*args, **kwargs)
            
            # Sending a signal (make sure to import Signal from django.dispatch)
            Signal().send(sender=self.__class__, user=user, request=self.request)
            
            # Generating OTP and setting expiration time
            otp = random.randint(1000, 9999)
            otp_expiry = datetime.now() + timedelta(minutes=3)
            user.otp = otp
            user.otp_expiry = otp_expiry
            user.save()  # Save the user instance with the OTP and expiry
            
            # Sending an activation email (assuming ActivationEmail is defined)
            context = {"user": user}
            to = [user.email]  # Assuming user.email contains the email address
            ActivationEmail(self.request, context).send(to)
            
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        # except Exception as e:
        #     user.delete()
        #     return Response({"message": "Check your internet connection"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

    def perform_update(self, serializer):
        super().perform_update(serializer)
        user = serializer.instance
        Signal().send(sender=self.__class__, user=user, request=self.request)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if instance == user:
            Token.objects.filter(user=user).delete()
            Signal.send(sender=user.__class__, request=request, user=user)
            logout(request)
            self.perform_destroy(instance)
            return Response(status=200)
        return Response(status=204)
    
    @action(["post"], detail=False)
    def login(self, request, *args, **kwargs):
        
        """
            Use this endpoint to obtain user authentiation token
        """
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)

            return Response(data={
                "message": "Login Successfully", 
                "tokens": tokens
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "invalid user details"}, status=status.HTTP_400_BAD_REQUEST)

        # serializer = self.get_serializer(data=request.data)
        # if serializer.is_valid():
        #     try:
        #         Signal().send(sender=user.__class__, request=request, user=user)
        #         return Response(data=TokenSerializer(token).data, status=200)
        #     except Exception as e:

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    @action(["post"], detail=True)
    def verify_otp(self, request, *args, **kwargs):
        id = kwargs["pk"]
        instance = User.objects.get(id=id)
        if (
            not instance.is_active
            and instance.otp == request.data.get("otp")
            and instance.otp_expiry
            and timezone.now() < instance.otp_expiry
        ):
            instance.is_active = True
            instance.otp_expiry = None
            instance.max_otp_try = settings.MAX_OTP_TRY
            instance.otp_max_out = None
            instance.save()
            return Response(
                {"message": "Successfully verified the user."}, status=status.HTTP_200_OK
            )
        return Response({
            "message": "User active or Please enter the correct OTP."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(["post"], detail=True)    
    def generate_otp(self, request, *args, **kwargs):
        """
        Regenerate OTP for the given user and send it to the user.
        """
        
        id = kwargs["pk"]
        try:
            user = User.objects.get(id=id)
            print(user)
            if int(user.max_otp_try) == 0 and timezone.now() < user.otp_max_out:
                return Response(
                    "Max OTP try reached, try after an hour",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            otp = random.randint(1000, 9999)
            otp_expiry = timezone.now() + timedelta(minutes=3)
            max_otp_try = int(user.max_otp_try) - 1

            user.otp = otp
            user.otp_expiry = otp_expiry
            user.max_otp_try = max_otp_try
            if max_otp_try == 0:
                # Set cool down time
                otp_max_out = timezone.now() + timedelta(hours=1)
                user.otp_max_out = otp_max_out
                return Response("You have exceeded otp trial times, retry again after one hour")
            elif max_otp_try == -1:
                user.max_otp_try = settings.MAX_OTP_TRY
            else:
                user.otp_max_out = None
                user.max_otp_try = max_otp_try
            user.save()

            Signal().send(sender=user.__class__)
            context = {"user": user}
            to = [user.email]
            ResendCodeEmail(self.request, context).send(to)
            return Response({"message":"Successfully generate new OTP."}, status=status.HTTP_200_OK)
        except NotFound: 
            return Response({"message": "Error occur while trying to create otp"}, status=status.HTTP_400_BAD_REQUEST)
        

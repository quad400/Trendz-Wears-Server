import random
from datetime import datetime, timedelta
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.contrib.auth import get_user_model, authenticate

from django.db import IntegrityError, transaction

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token

from core.constants import Messages

User = get_user_model()


class UserCreateMixin:
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            Response({'message': Messages.CANNOT_CREATE_USER_ERROR}, status=400)

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            otp = random.randint(1000, 9999)
            name = validated_data.pop("name")
            otp_expiry = datetime.now() + timedelta(minutes=3)
            user = User.objects.create_user(**validated_data)
            user.name = name
            user.is_active = False
            user.otp = otp
            user.otp_expiry = otp_expiry

            user.save(update_fields=["is_active"])
        return user


class UserCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields =(
            "id",
            "email",
            "name",
            "password",
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")
        attrs = super().validate(attrs)
        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        return attrs
    
    # def create(self, validated_data):
    #     name = validated_data.get("name")
    #     user = super().create(validated_data)
    #     return user.save(name=name)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "profile_image",)


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=4)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=False, style={"input_type": "password"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        password = attrs["password"]
        email = attrs["email"]
        self.user = authenticate(
            request=self.context.get("request"), email=email, password=password 
        )
        if not self.user:
            self.user = User.objects.filter(email=email).first()
            if self.user and not self.user.check_password(password):
                return Response({"message": Messages.INVALID_CREDENTIALS_ERROR})
        if self.user and self.user.is_active:
            return attrs
        return Response({"message": Messages.INVALID_CREDENTIALS_ERROR})
    
    
class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")

    class Meta:
        model = Token
        fields = ("auth_token",)
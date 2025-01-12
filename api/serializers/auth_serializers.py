from rest_framework_simplejwt.tokens import RefreshToken
from typing import Any, Dict, TypeVar
from rest_framework_simplejwt.models import TokenUser
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, update_last_login
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, PasswordField
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from main.views.auth_views import send_verification_email_to_user
from ..models import RefreshTokenUsage
from rest_framework_simplejwt.settings import api_settings
from main.models import School
from django.db import transaction
from djoser.serializers import UserCreateSerializer

from main.models import School, User

AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""
    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # token["is_superuser"] = user.is_superuser
        user_school: School | None = School.get_user_school(user)
        if user_school:
            token["school_name"] = str(user_school.name)
            token["school_short_name"] = str(
                user_school.short_name)

            if user_school.logo:
                token["school_logo"] = str(user_school.logo.url)
        else:
            token["school_logo"] = ""
            token["school_name"] = ""
            token["school_short_name"] = ""

        token["username"] = user.username
        token["email"] = user.email

        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        # Safely access image URL
        token['image'] = user.image.url if user.image else None
        token['gender'] = user.gender
        token['phone'] = user.phone
        token['role'] = user.role
        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        print(attrs)
        refresh = self.token_class(attrs["refresh"])
        # print(refresh.payload)

        data = {"access": str(refresh.access_token)}

        # Decode the refresh token to get the user ID
        try:
            payload = refresh.payload
            # Assuming 'user_id' is the key for the user ID in the payload
            user_id = payload['user_id']
        except KeyError:
            raise serializers.ValidationError("Invalid refresh token.")

        # Fetch the user from the database
        User = get_user_model()
        user = User.objects.get(id=user_id)

        TIME_RANGE_SECONDS = 3600  # 1 hour reuse range
        valid_token = RefreshTokenUsage.get_valid_token(
            user, TIME_RANGE_SECONDS)

        if valid_token:
            # Reuse the existing refresh token
            access_token = str(refresh.access_token)
            return {
                "access": access_token,
                "refresh": valid_token,
            }
        else:
            if api_settings.ROTATE_REFRESH_TOKENS:
                # If no valid token, proceed with the default behavior and rotation
                data = super().validate(attrs)

                # Save the new refresh token in the database
                RefreshTokenUsage.objects.create(
                    user=user,
                    refresh_token=data["refresh"],
                )
                if api_settings.BLACKLIST_AFTER_ROTATION:

                    try:
                        # Attempt to blacklist the given refresh token
                        refresh.blacklist()
                    except AttributeError:
                        # If blacklist app not installed, `blacklist` method will
                        # not be present
                        pass

                refresh.set_jti()
                refresh.set_exp()
                refresh.set_iat()

                data["refresh"] = str(refresh)

        return data


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'gender']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        # Validate email format
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_password(self, value):
        # Validate password strength
        try:
            validate_password(value)
        except ValidationError as ve:
            raise serializers.ValidationError(str(ve))
        return value

    def create(self, validated_data):
        with transaction.atomic():
            try:
                req = self.context['request']

                # Handle user registration
                user = User.objects.create(
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    email=validated_data['email'],
                    gender=validated_data['gender'],
                    role="owner",
                )
                user.set_password(validated_data['password'])
                user.save()

                # Create the School
                school_data = {
                    'name': req.data.get('school_name'),
                    'phone': req.data.get('school_phone'),
                    'email': req.data.get('school_email'),
                }
                school_serializer = SchoolRegistrationSerializer(
                    data=school_data)

                school_serializer.is_valid(raise_exception=True)
                school = school_serializer.save(owner=user)

                user.school = school
                user.save()

                if user.is_admin:  # Assuming you have an is_admin attribute for the user
                    send_verification_email_to_user(
                        User, user, self.context['request'])

                return user
            except Exception as e:
                raise serializers.ValidationError(str(e))

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs


class SchoolRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['name', 'phone', 'email']

    def validate_email(self, value):
        # Validate school email format
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid school email format.")
        return value

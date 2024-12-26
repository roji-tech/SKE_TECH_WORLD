from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, Token, UntypedToken
from ..models import RefreshTokenUsage
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.settings import api_settings

from main.models import School, Teacher

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["is_superuser"] = user.is_superuser
        token["is_staff"] = user.is_staff
        return token


class UserRegistrationSerializer(serializers.ModelSerializer):
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

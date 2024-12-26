from rest_framework import serializers
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
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["image"] = user.image
        token["gender"] = user.gender
        token["phone"] = user.phone
        token["role"] = user.role
        # token["is_superuser"] = user.is_superuser
        # token["is_staff"] = user.is_staff
        print(token)
        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])
        print(refresh.payload)

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


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class CreateTeacherSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    school_id = serializers.IntegerField()
    department = serializers.CharField(
        max_length=24, required=False, allow_blank=True)

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with this id does not exit')
        return value

    def validate_school_id(self, value):
        try:
            school = School.objects.get(id=value)
        except School.DoesNotExist:
            raise serializers.ValidationError(
                'School with this id does not exit')
        return value

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['user_id'])
        school = School.objects.get(id=validated_data['school_id'])
        department = validated_data.get('department', '')

        teacher = Teacher.objects.create(
            user=user,
            school=school,
            department=department
        )
        return teacher

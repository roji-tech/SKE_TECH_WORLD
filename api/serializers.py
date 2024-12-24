from rest_framework import serializers
from main.models import School, AcademicSession, Term, SchoolClass, Teacher

from main.models import School
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, Token, UntypedToken
from .models import RefreshTokenUsage
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.settings import api_settings


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

class SchoolClassSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = SchoolClass
        fields = [
            'id',
            'name',
            'name_display',
            'division',
            'category',
            'category_display',
            'academic_session',
            'class_teacher',
        ]

class SchoolSerializer(serializers.ModelSerializer):
  classes = SchoolClassSerializer(read_only=True, many=True)
  
  class Meta:
    model = School
    fields  = ['id', 'name','classes', 'owner', 'address', 'phone', 'email', 'logo'] 


class AcademicSessionSerializer(serializers.ModelSerializer):
  school = SchoolSerializer(read_only=True)

  class Meta:
    model = AcademicSession
    fields = ['id','name', 'school', 'start_date', 'end_date', 'is_current', 'next_session_begins']

    # def get_school(self, obj):
    #   return str(obj.school.name)

class TermSerializer(serializers.ModelSerializer):
  class Meta:
    model = Term
    fields = ['academic_session', 'name', 'start_date', 'end_date']

    def create(self, validated_data):
      academic_session_id = self.context['academic_session_id']
      return Term.objects.create(academic_session_id=academic_session_id, **validated_data)



    class Meta:
        model = School
        fields = '__all__'



class TeacherSerializer(serializers.ModelSerializer):
    # Nested serialization for related user fields
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = Teacher
        fields = [
            'id',
            'user',  # User ID reference
            'user_full_name',
            'user_email',
            'user_phone',
            'school',
            'department',
        ]


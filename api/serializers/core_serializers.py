from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, Token, UntypedToken
from ..models import RefreshTokenUsage
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.settings import api_settings

from main.models import School, Teacher, SchoolClass, AcademicSession, Term, LessonPlan, Subject, Student

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
        token["image"] = user.image.url if user.image else None
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


class SchoolClassSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(
        source='get_name_display', read_only=True)
    category_display = serializers.CharField(
        source='get_category_display', read_only=True)
    # class_capacity = serializers.SerializerMethodField(method_name='get_class_capacity')

    class Meta:
        model = SchoolClass
        fields = [
            'id',
            'name',
            'name_display',
            'division',
            'category',
            'class_capacity',
            'category_display',
            'academic_session',
            'class_teacher',
        ]


class SchoolSerializer(serializers.ModelSerializer):
    #   classes = SchoolClassSerializer(read_only=True, many=True)

    class Meta:
        model = School
        fields = ['id', 'name', 'owner', 'address', 'phone', 'email', 'logo']


class AcademicSessionSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = AcademicSession
        fields = ['id', 'name', 'school', 'start_date',
                  'end_date', 'is_current', 'next_session_begins']

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
    class Meta:
        model = Teacher
        fields = '__all__'


# class CreateTeacherSerializer(serializers.Serializer):
#     user_id = serializers.IntegerField()
#     school_id = serializers.IntegerField()
#     department = serializers.CharField(
#         max_length=24, required=False, allow_blank=True)

#     def validate_user_id(self, value):
#         try:
#             user = User.objects.get(id=value)
#         except User.DoesNotExist:
#             raise serializers.ValidationError(
#                 'User with this id does not exit')
#         return value

#     def validate_school_id(self, value):
#         try:
#             school = School.objects.get(id=value)
#         except School.DoesNotExist:
#             raise serializers.ValidationError(
#                 'School with this id does not exit')
#         return value

#     def create(self, validated_data):
#         user = User.objects.get(id=validated_data['user_id'])
#         school = School.objects.get(id=validated_data['school_id'])
#         department = validated_data.get('department', '')

#         teacher = Teacher.objects.create(
#             user=user,
#             school=school,
#             department=department
#         )
#         return teacher

class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(
        method_name='get_student_full_name')
    session_admitted = serializers.SerializerMethodField(
        method_name='get_formatted_admission_date')

    class Meta:
        model = Student
        fields = ['student_id', 'reg_no', 'school', 'session_admitted',
                  'full_name', "date_of_birth", 'student_class']

    def get_student_full_name(self, obj):
        return obj.get_full_name()

    def get_formatted_admission_date(self, obj):
        return obj.session_admitted.strftime('%d-%b-%Y')


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'teacher']


class LessonPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlan
        fields = ['title', 'school_class', 'subject',
                  'uploaded_file', 'uploaded_by']

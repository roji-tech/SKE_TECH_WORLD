import django.db
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, Token, UntypedToken

from main.models.users import TEACHER
from ..models import RefreshTokenUsage
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.settings import api_settings

from main.models import User, School, Teacher, SchoolClass, AcademicSession, Term, LessonPlan, Subject, Student


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


class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'gender', 'email', 'phone', 'image']


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'department']

    def create(self, validated_data):
        with transaction.atomic():
            request = self.context.get('request')
            school = School.get_user_school(request.user)
            user_data = validated_data.pop('user')
            user = User.objects.create(
                **user_data, role=TEACHER, school=school)
            user.set_password(user.last_name)
            user.save()

            print(school)

            teacher = Teacher.objects.create(
                user=user, school=school,
                **validated_data
            )
            # teacher.save()
        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for field, value in user_data.items():
                setattr(instance.user, field, value)
            instance.user.save()
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

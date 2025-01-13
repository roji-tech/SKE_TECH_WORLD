import django.db
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, Token, UntypedToken

from main.models.users import TEACHER, STUDENT
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.settings import api_settings

from main.models import User, School, Teacher, SchoolClass, AcademicSession, Term, LessonPlan, Subject, Student
from main.models.models import School


class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'gender', 'email', 'phone', 'image']


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
    # owner = UserSerializer()

    class Meta:
        model = School
        fields = ['id', 'name', 'address', 'phone', 'email',
                  'logo', "short_name", "code", "website", "motto", "about",]


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ['academic_session', 'name', 'start_date', 'end_date']

        def create(self, validated_data):
            academic_session_id = self.context['academic_session_id']
            return Term.objects.create(academic_session_id=academic_session_id, **validated_data)


class AcademicSessionSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    terms = TermSerializer(read_only=True, many=True)

    class Meta:
        model = AcademicSession
        fields = ['id', 'name', 'school', 'start_date', 'terms',
                  'end_date', 'is_current', 'next_session_begins']
        read_only_fields = ['name', 'is_current', 'school_name']

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

        # def get_school(self, obj):
        #   return str(obj.school.name)


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

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'teacher', 'school_class']





class LessonPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlan
        fields = ['title', 'school_class', 'subject',
                  'uploaded_file', 'uploaded_by']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # full_name = serializers.SerializerMethodField(
    #     method_name='get_student_full_name')

    class Meta:
        model = Student
        fields = ['user', 'reg_no', 'school', 'session_admitted',
                  "date_of_birth", 'student_class']


class StudentCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    session_admitted = serializers.SerializerMethodField(
        method_name='get_formatted_admission_date')

    class Meta:
        model = Student
        fields = ['user', 'reg_no', 'session_admitted',
                  "date_of_birth", 'student_class']

    def create(self, validated_data):
        with transaction.atomic():
            request = self.context.get('request')
            school = request.school
            print(school)

            user_data = validated_data.pop('user')
            user_data['role'] = STUDENT
            user_data['school'] = school
            user = User.objects.create(**user_data)
            user.set_password(str(user.last_name).lower())
            user.save()


            validated_data['school'] = school
            validated_data['user'] = user
            student = Student.objects.create(**validated_data)
        return student

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

    def get_student_full_name(self, obj):
        return obj.get_full_name()

    def get_formatted_admission_date(self, obj):
        try:
            return obj.session_admitted.strftime('%d-%b-%Y')
        except:
          return None

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'department']

    def create(self, validated_data):
        with transaction.atomic():
            request = self.context.get('request')
            school = request.school
            user_data = validated_data.pop('user')

            user_data['role'] = TEACHER
            user_data['school'] = school
            user = User.objects.create(**user_data)
            user.set_password(str(user.last_name).lower())
            user.save()

            print(school)

            validated_data['school'] = school
            validated_data['user'] = user
            teacher = Teacher.objects.create(**validated_data)
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

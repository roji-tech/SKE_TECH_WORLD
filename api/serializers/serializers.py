from rest_framework import serializers
from django.contrib.auth import get_user_model

from main.models import School, Teacher

User = get_user_model()


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

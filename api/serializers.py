from rest_framework import serializers
from main.models import School, AcademicSession, Term, SchoolClass

from main.models import School
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
    fields  = ['id'] 


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

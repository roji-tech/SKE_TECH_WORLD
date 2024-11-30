from rest_framework import serializers
from main.models import School, AcademicSession, Term



class SchoolSerializer(serializers.ModelSerializer):
  class Meta:
    model = School
    fields  = '__all__'

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

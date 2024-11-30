from django.shortcuts import render


from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from main.models import School, AcademicSession, Term
from api.serializers import AcademicSessionSerializer, SchoolSerializer, TermSerializer




class SchoolViewSet(ModelViewSet):
  queryset = School.objects.all()
  serializer_class  = SchoolSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]



class AcademicSessionViewSet(ModelViewSet):
  serializer_class = AcademicSessionSerializer
  queryset = AcademicSession.objects.all()


class TermViewSet(ModelViewSet):
  serializer_class = TermSerializer
  queryset = Term.objects.all()

  # def get_queryset(self, request):
  #   return Term.objects.filter(academic_session_pk=self.kwargs['academic_session_pk'])
  
  # def get_serializer_context(self):
  #   return {'academic_session_id' : self.kwargs['academic_session_pk']}
  
  def get_queryset(self):
      academic_session_id = self.kwargs.get('academic_session_pk')
      if academic_session_id:
          return self.queryset.filter(academic_session_id=academic_session_id)
      return self.queryset

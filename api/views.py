from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render


from rest_framework.viewsets import ModelViewSet

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from main.models import School, AcademicSession, Term, SchoolClass, Teacher, Subject, Student
from api.serializers import AcademicSessionSerializer, SchoolClassSerializer, SchoolSerializer, TermSerializer, StudentSerializer


from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView




from .serializers import *



class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom

    # serializer_class = ExampleTokenObtainPairSerializer
    
    serializer_class = CustomTokenObtainPairSerializer



class LogoutView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, TokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SchoolViewSet(ModelViewSet):
  queryset = School.objects.all()
  serializer_class  = SchoolSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]


class SchoolClassViewSet(ModelViewSet):
   queryset = SchoolClass.objects.all()
   serializer_class = SchoolClassSerializer

   def get_queryset(self):
      user = self.request.user
      school = School.get_user_school(user=user)
      return SchoolClass.objects.filter(academic_session__school=school)




class AcademicSessionViewSet(ModelViewSet):
  serializer_class = AcademicSessionSerializer
  queryset = AcademicSession.objects.all()


class TermViewSet(ModelViewSet):
  serializer_class = TermSerializer
  queryset = Term.objects.all()

  def get_queryset(self):
      academic_session_id = self.kwargs.get('academic_session_pk')
      if academic_session_id:
          return self.queryset.filter(academic_session_id=academic_session_id)
      return self.queryset


  # def get_queryset(self, request):
  #   return Term.objects.filter(academic_session_pk=self.kwargs['academic_session_pk'])
  
  # def get_serializer_context(self):
  #   return {'academic_session_id' : self.kwargs['academic_session_pk']}
  
class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all().select_related('user', 'school')
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
   


class CreateTeacherView(APIView):
    def post(self, request):
        serializer = CreateTeacherSerializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.save()
            return Response({'message' : 'Teacher added successfully', 'teacher_id' : teacher.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import api_view, renderer_classes

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


from main.views.auth_views import send_verification_email_to_user
from .serializers import (
    CreateTeacherSerializer, CustomTokenObtainPairSerializer, SchoolSerializer, TeacherSerializer,
    SchoolRegistrationSerializer,                          UserRegistrationSerializer)
from main.models import School, Teacher

import logging

logger = logging.getLogger(__name__)


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


class RegisterAndRegisterSchoolView(APIView):
    serializer_class = UserRegistrationSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    permission_classes = [AllowAny]  # Adjust permission as necessary

    def get(self, request, *args, **kwargs):
        user_serializer = UserRegistrationSerializer()
        school_serializer = SchoolRegistrationSerializer()

        # Return initial empty forms for HTML rendering
        return Response({
            "data_input": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.does@example.com",
                "password": "StrongPassword123!",
                "gender": "M",
                "school_name": "Sample School",
                "school_phone": "1234567890",
                "school_email": "contact-us@sampleschool.com"
            },
            "message": "Use POST to register."
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Handle user registration
        user_serializer = UserRegistrationSerializer(data=request.data)

        if user_serializer.is_valid():
            # Create the User
            owner = user_serializer.save()
            owner.set_password(user_serializer.validated_data['password'])
            owner.save()

            # Create the School
            school_data = {
                'name': request.data.get('school_name'),
                'phone': request.data.get('school_phone'),
                'email': request.data.get('school_email'),
            }
            school_serializer = SchoolRegistrationSerializer(data=school_data)

            if school_serializer.is_valid():
                school = school_serializer.save(owner=owner)

                if owner.is_admin:  # Assuming you have an is_admin attribute for the user
                    send_verification_email_to_user(User, owner, request)

                # Generate tokens
                refresh = RefreshToken.for_user(owner)
                access = str(refresh.access_token)

                return Response({
                    "status": True,
                    "message": "Account created successfully.",
                    "tokens": {
                        "refresh": str(refresh),
                        "access": access
                    }
                }, status=status.HTTP_201_CREATED)

            return Response({"status": False, "message": school_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": False, "message": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        response.data['status'] = False
        return response


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
            return Response({'message': 'Teacher added successfully', 'teacher_id': teacher.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

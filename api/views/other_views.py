import re
import jwt

from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.module_loading import import_string

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import api_view, renderer_classes

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, Token, UntypedToken
from rest_framework_simplejwt.views import TokenObtainPairView

from main.views.auth_views import send_verification_email_to_user
from main.models import User, School, Teacher, AcademicSession, Term, SchoolClass, Student, Subject
from django.db import transaction
from djoser.views import UserViewSet as DjoserUserViewSet

from .serializers import (
    CustomTokenObtainPairSerializer,
    SchoolSerializer,
    TeacherSerializer,
    SchoolClassSerializer,
    AcademicSessionSerializer,
    StudentSerializer,
    TermSerializer,
    SubjectSerializer,
    UserRegistrationSerializer,
    SchoolRegistrationSerializer,
)
from .permissions import IsAdminOrIsTeacherOrReadOnly, IsAdminOrReadOnly


class SchoolViewSet(ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SchoolClassViewSet(ModelViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        school = School.get_user_school(user=user)
        return SchoolClass.objects.filter(academic_session__school=school)


class AcademicSessionViewSet(ModelViewSet):
    serializer_class = AcademicSessionSerializer
    queryset = AcademicSession.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class TermViewSet(ModelViewSet):
    serializer_class = TermSerializer
    queryset = Term.objects.all()
    permission_classes = [IsAuthenticated]

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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['GET', 'PUT'])
    def me(self, request):
        if request.method == 'GET':
            (teacher, created) = Teacher.objects.get_or_create(
                teacher_id=request.user.id)
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = TeacherSerializer(teacher)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrIsTeacherOrReadOnly]

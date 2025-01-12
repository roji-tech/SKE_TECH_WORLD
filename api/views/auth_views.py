from math import perm
from django.shortcuts import render
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
from rest_framework.decorators import api_view, renderer_classes, permission_classes

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, Token, UntypedToken
from rest_framework_simplejwt.views import TokenObtainPairView

from main.views.auth_views import send_verification_email_to_user
from main.models import User, School, Teacher, AcademicSession, Term, SchoolClass, Student, Subject
from django.db import transaction
from djoser.views import UserViewSet as DjoserUserViewSet

from api.serializers import SchoolSerializer
from ..permissions import IsAdminOrIsTeacherOrReadOnly, IsAdminOrReadOnly


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


@permission_classes([AllowAny])
@api_view(['GET'])
def get_school_info(request, school_code):
    school = request.school
    print("School", school)
    serializer = SchoolSerializer(school)
    return Response(serializer.data)

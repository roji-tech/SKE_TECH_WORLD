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

from ..serializers import (
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


# class CustomUserViewSet(DjoserUserViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserRegistrationSerializer

#     @action(detail=False, methods=['GET'])
#     def me(self, request, *args, **kwargs):
#         user = request.user
#         serializer = self.get_serializer(user)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         user_serializer = UserRegistrationSerializer(
#             data=request.data, context={'request': request})
#         user_serializer.is_valid(raise_exception=True)
#         self.perform_create(user_serializer)
#         # send_verification_email_to_user(user)
#         headers = self.get_success_headers(user_serializer.data)
#         return Response(user_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#         # if user_serializer.is_valid():
#         #     result = user_serializer.save()

#         #     if result["status"]:
#         #         # Generate tokens
#         #         user = User.objects.get(email=request.data['email'])
#         #         # refresh = RefreshToken.for_user(user)
#         #         # access = str(refresh.access_token)

#         #         return Response({
#         #             "status": True,
#         #             "message": result["message"],
#         #             # "tokens": {
#         #             #     "refresh": str(refresh),
#         #             #     "access": access
#         #             # }
#         #         }, status=status.HTTP_201_CREATED)

#         #     return Response({"status": False, "message": result["message"]}, status=status.HTTP_400_BAD_REQUEST)

#         # print(user_serializer.errors)
#         # print(user_serializer.error_messages)

#         # return Response({"status": False, "message": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


#


# class RegisterAndRegisterSchoolView(APIView):
#     serializer_class = UserRegistrationSerializer
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
#     # Adjust permission as necessary
#     permission_classes = [AllowAny]

#     def get(self, request, *args, **kwargs):
#         user_serializer = UserRegistrationSerializer()
#         school_serializer = SchoolRegistrationSerializer()

#         # Return initial empty forms for HTML rendering
#         return Response({
#             "data_input": {
#                 "first_name": "John",
#                 "last_name": "Doe",
#                 "email": "john.does@example.com",
#                 "password": "StrongPassword123!",
#                 "gender": "M",
#                 "school_name": "Sample School",
#                 "school_phone": "1234567890",
#                 "school_email": "contact-us@sampleschool.com"
#             },
#             "message": "Use POST to register."
#         }, status=status.HTTP_200_OK)

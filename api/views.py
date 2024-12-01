from django.shortcuts import render


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from main.models import School
from api.serializers import SchoolSerializer



class SchoolViewSet(ModelViewSet):
  queryset = School.objects.all()
  serializer_class  = SchoolSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]

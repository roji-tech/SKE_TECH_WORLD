from django.db import models
from django.utils import timezone

from main.models.models import School

# Create your models here.

class Notification(models.Model):
      title = models.CharField(max_length=255)
      message = models.TextField()
      icon = models.CharField(max_length=50)  # Optional field for icons like 'person_add', 'assessment', etc.
      created_at = models.DateTimeField(default=timezone.now)

      def __str__(self):
       return f"{self.title} - {self.created_at}"


      @classmethod
      def get_school_events(cls, request):
          user = request.user
          school = School.get_user_school(user)
          """Return all events for a specific school"""
          return cls.objects.filter(school=school)

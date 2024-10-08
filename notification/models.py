from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from main.models.models import School

# Create your models here.

class Notification(models.Model):
      title = models.CharField(max_length=255)
      message = models.TextField()
      icon = models.CharField(max_length=50, blank=True)  # Optional field for icons like 'person_add', 'assessment', etc.
      created_at = models.DateTimeField(default=timezone.now)
      user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_("User"), on_delete=models.CASCADE)

      def __str__(self):
       return f"{self.title} - {self.created_at}"


      

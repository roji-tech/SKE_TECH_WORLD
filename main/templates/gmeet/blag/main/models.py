from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=30)


# Create your models here.
class BlogPost(models.Model):
    headline = models.CharField(max_length=30)
    content = models.TextField
    is_public = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
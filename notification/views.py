from django.shortcuts import render
from .models import Notification
# Create your views here.
def notification_center(request):
  notifications = Notification.objects.filter(user=request.user).order_by('-created_by')
  return {'notifications' : notifications}
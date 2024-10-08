# views.py
from django.shortcuts import render
from .models import Notification

def notification_center(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notification/notification_center.html', {'notifications': notifications})

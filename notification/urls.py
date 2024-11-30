from django.urls import path
from . import views

urlpatterns = [
  path('', views.notification_center, name='notifications')
]
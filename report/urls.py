from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_complaint, name='complaints'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
]

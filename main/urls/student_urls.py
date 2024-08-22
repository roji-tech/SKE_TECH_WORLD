from django.urls import path
from ..views import StudentsHome

urlpatterns = [
    path('students/', StudentsHome.as_view(), name='students_home'),
]
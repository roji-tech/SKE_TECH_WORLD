from django.urls import path
from ..views import StudentHome

urlpatterns = [
    path('students-home/', StudentHome.as_view(), name='students_home'),
]
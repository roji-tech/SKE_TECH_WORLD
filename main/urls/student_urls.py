from django.urls import path
from ..views import StudentsHome

urlpatterns = [
    path('students-home/', StudentsHome.as_view(), name='students_home'),
]
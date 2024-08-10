from django.urls import path
from main.views.teacher_views import TeachersHome

urlpatterns = [
    path('teacher_index/', TeachersHome.as_view(), name='teachers_home'),
    # path('myview/', TeachersHome.as_view(), name='teachers_home'),
    # path('myview/', TeachersHome.as_view(), name='teachers_home'),
]
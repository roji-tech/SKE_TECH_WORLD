from django.urls import path
from .. import views
from main.views.teacher_views import TeachersHome

urlpatterns = [
    path('teacher-index/', TeachersHome.as_view(), name='teachers_home'),
    path('add-gmeet/', views.uploadgmeet, name='gmeet'),
    path('edit-gmeet/', views.editgmeet, name='edit_gmeet'),
    # path('myview/', TeachersHome.as_view(), name='teachers_home'),
]
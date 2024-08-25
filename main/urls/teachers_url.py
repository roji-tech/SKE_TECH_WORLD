from django.urls import path
from .. import views

urlpatterns = [
    path('teachers/', views.TeachersHome.as_view(), name='teachers_home'),
    path('add-gmeet/', views.addgmeet, name='add_gmeet'),
    path('edit-gmeet/', views.editgmeet, name='edit_gmeet'),
    path('upload-lesson/', views.upload_lesson_plan, name='upload_lesson_plan'),
    path('lessons-lists/', views.lessons_list, name='lessons_lists'),
]

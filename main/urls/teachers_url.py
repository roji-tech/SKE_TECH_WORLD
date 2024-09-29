from django.urls import path
from .. import views

auth_urlpatterns = [
    path('teachers/', views.TeachersHome.as_view(), name='teachers'),

    # path('teachers/add-gmeet/', views.add_gmeet, name='add_gmeet'),
    # path('teachers/edit-gmeet/', views.teachers_edit_gmeet, name='edit_gmeet'),

    # path('teachers/upload-lesson/', views.upload_lesson_plan,
    #      name='upload_lesson_plan'),
    # path('teachers/lessons-lists/', views.lessons_list, name='lessons_lists'),

    # path('teachers/add-assessment/', views.continous_assessment_view, name='continous-assessment'),
]

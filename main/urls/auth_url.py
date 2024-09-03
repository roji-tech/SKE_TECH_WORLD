from django.urls import path
from main.views import login_views

urlpatterns = [
    path(
        'admin/login/',
        login_views.AdminLoginView.as_view(),
        name='admin-login'
    ),
    path(
        'skesuperadmin/login',
        login_views.SuperAdminLoginView.as_view(),
        name='superadmin-login'
    ),

    path(
        'teachers/login/',
        login_views.TeacherLoginView.as_view(),
        name='teacher-login'
    ),
    path(
        'students/login/',
        login_views.StudentLoginView.as_view(),
        name='student-login'
    ),
    #     path('teachers/edit-gmeet/', views.teachers_edit_gmeet, name='edit_gmeet'),

    #     path('teachers/upload-lesson/', views.upload_lesson_plan,
    #          name='upload_lesson_plan'),
    #     path('teachers/lessons-lists/', views.lessons_list, name='lessons_lists'),

    # path('teachers/add-assessment/', views.continous_assessment_view, name='continous-assessment'),
]
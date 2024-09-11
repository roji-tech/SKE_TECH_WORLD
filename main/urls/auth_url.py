from django.contrib.auth import views
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

# The views used below are normally mapped in the AdminSite instance.
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.


urlpatterns += [
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

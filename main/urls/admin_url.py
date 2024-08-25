from django.urls import path
from main.views.admin_views import AddSession, ClassCreateView, ClassDeleteView, ClassListView, ClassUpdateView, DeleteSession, ListSession, UpdateSession
from ..views import AdminsHome, RegisterSchool, AdminLogin, AdminsHelp

urlpatterns = [
    path('admin/', AdminsHome.as_view(), name='myadmin'),
    path('admin/register/', RegisterSchool.as_view(), name='register-school'),
    path('admin/login/', AdminLogin.as_view(), name='admin-login'),
    path('admin/help/', AdminsHelp.as_view(), name='admin-help'),

    # ACADEMIC SESSIONS
    path('admin/sessions/', ListSession.as_view(), name='list-sessions'),
    path('admin/add-session/', AddSession.as_view(), name='add-session'),
    path('admin/session/<int:pk>/update/',
         UpdateSession.as_view(), name='update-session'),
    path('admin/session/<int:pk>/delete',
         DeleteSession.as_view(), name='delete-session'),

    # CLASSES
    path('admin/classes/', ClassListView.as_view(), name='list-classes'),
    path('admin/add-class/', ClassCreateView.as_view(), name='add-class'),
    path('admin/classes/<int:pk>/update/',
         ClassUpdateView.as_view(), name='update-class'),
    path('admin/classes/<int:pk>/delete',
         ClassDeleteView.as_view(), name='delete-class'),

    path("",  ClassCreateView.as_view(), name="add-student"),
    path("",  ClassCreateView.as_view(), name="list-students"),

    path("",  ClassCreateView.as_view(), name="add-subject"),
    path("",  ClassCreateView.as_view(), name="list-subjects"),

    path("",  ClassCreateView.as_view(), name="add-teacher"),
    path("",  ClassCreateView.as_view(), name="list-teachers"),

    path("",  ClassCreateView.as_view(), name="add-subject"),
    path("",  ClassCreateView.as_view(), name="list-subjects"),
]

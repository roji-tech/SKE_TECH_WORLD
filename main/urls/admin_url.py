from django.urls import path
from main.views.admin_views import AddSession, ClassCreateView, ClassListView, DeleteSession, ListSession, UpdateSession
from ..views import AdminsHome, RegisterSchool, AdminLogin, AdminsHelp


urlpatterns = [
    path('admin/', AdminsHome.as_view(), name='myadmin'),
    path('admin/register/', RegisterSchool.as_view(), name='register-school'),
    path('admin/login/', AdminLogin.as_view(), name='admin-login'),
    path('admin/help/', AdminsHelp.as_view(), name='admin-help'),

    # ACADEMIC SESSIONS
    path('admin/add-session/', AddSession.as_view(), name='add-session'),
    path('admin/list-sessions/', ListSession.as_view(), name='list-sessions'),
    path('admin/session/<int:pk>/update/',
         UpdateSession.as_view(), name='update-session'),
    path('admin/session/<int:pk>/delete',
         DeleteSession.as_view(), name='delete-session'),

    # CLASSES
    path('admin/add-class/', ClassCreateView.as_view(), name='add-class'),
    path('admin/list-classes/', ClassListView.as_view(), name='list-classes'),
    path('admin/classes/<int:pk>/update/',
         UpdateSession.as_view(), name='update-class'),
    path('admin/classes/<int:pk>/delete',
         DeleteSession.as_view(), name='delete-class'),

]

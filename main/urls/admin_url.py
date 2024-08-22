from django.urls import path
from main.views.admin_views import AddSession, ListSession
from ..views import AdminsHome, RegisterSchool, AdminLogin, AdminsHelp


urlpatterns = [
    path('admin/', AdminsHome.as_view(), name='myadmin'),
    path('admin/register/', RegisterSchool.as_view(), name='register-school'),
    path('admin/login/', AdminLogin.as_view(), name='admin-login'),
    path('admin/help/', AdminsHelp.as_view(), name='admin-help'),
    
    path('admin/add-session/', AddSession.as_view(), name='add-session'),
    path('admin/list-sessions/', ListSession.as_view(), name='list-sessions'),
]

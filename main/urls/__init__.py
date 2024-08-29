from .superadmin_url import urlpatterns as superadmins_urlpatterns
from .student_urls import urlpatterns as students_urlpatterns
from .admin_url import urlpatterns as admins_urlpatterns
from .teachers_url import urlpatterns as teachers_urlpatterns
from django.urls import path
from django.views.generic import TemplateView
from main.views.settings import SettingView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("settings/", SettingView.as_view(), name="settings")
]

urlpatterns += teachers_urlpatterns
urlpatterns += admins_urlpatterns
urlpatterns += students_urlpatterns
urlpatterns += superadmins_urlpatterns

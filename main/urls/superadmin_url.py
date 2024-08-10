from django.urls import path
from ..views import SuperAdminHome

urlpatterns = [
  path('', SuperAdminHome.as_view(), name='superadmin_index'),
]
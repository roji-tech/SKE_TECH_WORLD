from django.urls import path
from ..views import SuperadminHome

urlpatterns = [
  path('', SuperadminHome.as_view(), name='superadmin_index'),
]
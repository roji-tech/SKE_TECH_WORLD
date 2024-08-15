from django.urls import path
from ..views import AdminsHome


urlpatterns = [
    path('admins/', AdminsHome.as_view(), name='admins_home')
]

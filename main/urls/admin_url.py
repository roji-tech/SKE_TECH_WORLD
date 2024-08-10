from django.urls import path
from ..views import AdminHome
urlpatterns = [
path('admins-home/', AdminHome.as_view(), name='admins_home')
]

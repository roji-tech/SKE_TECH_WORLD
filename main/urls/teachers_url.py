from django.urls import path
from main.views.teacher_views import Home

urlpatterns = [
    path('', Home.as_view(), name='teachers_home'),
    path('myview/', Home.as_view(), name='teachers_home'),
    path('myview/', Home.as_view(), name='teachers_home'),
]
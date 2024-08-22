from django.urls import path
from .. import views
urlpatterns = [
path('admins-home/', views.AdminsHome.as_view(), name='admins_home'),
path('teachers-list/', views.teachers_list, name='teachers_list'),
path('add-teacher/', views.add_teacher, name='add_teacher'),


]

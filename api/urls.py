from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import token_refresh, token_verify, token_obtain_pair

from api.views import LogoutView
from . import views


router = DefaultRouter()
router.register('schools', views.SchoolViewSet, basename='schools')
router.register('teachers', views.TeacherViewSet, basename='teachers')


urlpatterns = [
    path('', include(router.urls)),
    path('create-teacher/', views.CreateTeacherView.as_view(), name='create-teacher'),

    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/logout/", LogoutView.as_view()),

    path("auth/login/", token_obtain_pair, name="token_obtain_pair"),
    path("auth/token/refresh/", token_refresh, name="token_refresh"),
    path("auth/token/verify/", token_verify, name="token_verify"),

    path('auth/register/', views.RegisterAndRegisterSchoolView.as_view(),
         name='register_school'),

]

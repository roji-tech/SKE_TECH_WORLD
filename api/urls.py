from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from api.views import CustomTokenObtainPairView, LogoutView
from . import views


router = DefaultRouter()
router.register('schools', views.SchoolViewSet, basename='schools')


urlpatterns = [
    path('', include(router.urls)),

    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/logout/", LogoutView.as_view()),

    path("auth/token/", CustomTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

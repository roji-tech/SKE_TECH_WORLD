from django.urls import path, include

from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from api.views import CustomTokenObtainPairView, LogoutView
from . import views


router = routers.DefaultRouter()
router.register('schools', views.SchoolViewSet, basename='schools'),
router.register('academic-sessions', views.AcademicSessionViewSet, basename='academic_session')
router.register('teachers', views.TeacherViewSet)

# domains_router = routers.NestedSimpleRouter(router, r'domains', lookup='domain')
# Nested routers for Academic sessiion
academic_sessions_router = routers.NestedDefaultRouter(router, 'academic-sessions', lookup='academic_session')
academic_sessions_router.register('terms', views.TermViewSet, basename='academic-session-terms')

# Nested Router for Schools
school_router = routers.NestedDefaultRouter(router, 'schools', lookup='school')
school_router.register('classes', views.SchoolClassViewSet, basename='school-classes')

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

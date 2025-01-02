from django.urls import path, include

from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import token_refresh, token_verify, token_obtain_pair

from api.views import LogoutView
from api.views.other_views import TeacherViewSet
from . import views


router = routers.DefaultRouter()
router.register('schools', views.SchoolViewSet, basename='schools'),
router.register('academic-sessions', views.AcademicSessionViewSet,
                basename='academic_session')
router.register('teachers', views.TeacherViewSet, basename='teachers')
router.register('students', views.StudentViewSet, basename='students')


# domains_router = routers.NestedSimpleRouter(router, r'domains', lookup='domain')
# Nested routers for Academic sessiion
academic_sessions_router = routers.NestedSimpleRouter(
    router, 'academic-sessions', lookup='academic_session')
academic_sessions_router.register(
    'terms', views.TermViewSet, basename='academic-session-terms')

# Nested Router for Schools
school_router = routers.NestedSimpleRouter(router, 'schools', lookup='school')
school_router.register('classes', views.SchoolClassViewSet,
                       basename='school-classes')
# # Nested Router for CustomUser
# user_router = routers.NestedSimpleRouter(router, 'users', lookup='user')
# user_router.register('custom', views.CustomUserViewSet, basename='user-custom')

router.register("auth/users", views.CustomUserViewSet)


router.register('teachers', TeacherViewSet, basename='teacher')

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    #     path('create-teacher/', views.CreateTeacherView.as_view(), name='create-teacher'),

    # path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/logout/", LogoutView.as_view()),

    path("auth/login/", token_obtain_pair, name="token_obtain_pair"),
    path("auth/token/refresh/", token_refresh, name="token_refresh"),
    path("auth/token/verify/", token_verify, name="token_verify"),

    # path('auth/register/', views.RegisterAndRegisterSchoolView.as_view(),
    #      name='register_school'),

]

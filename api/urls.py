from django.urls import path, include

from rest_framework_nested import routers


from . import views


router = routers.DefaultRouter()
router.register('schools', views.SchoolViewSet, basename='schools'),
router.register('academic-sessions', views.AcademicSessionViewSet, basename='academic_session')

# domains_router = routers.NestedSimpleRouter(router, r'domains', lookup='domain')

academic_sessions_router = routers.NestedDefaultRouter(router, 'academic-sessions', lookup='academic_session')

academic_sessions_router.register('terms', views.TermViewSet, basename='academic-session-terms')




urlpatterns = [
  path('v1/', include(router.urls))
]


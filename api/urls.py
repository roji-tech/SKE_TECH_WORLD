from django.urls import path, include

from rest_framework_nested import routers


from . import views


router = routers.DefaultRouter()
router.register('schools', views.SchoolViewSet, basename='schools'),
router.register('academic-sessions', views.AcademicSessionViewSet, basename='academic_session')

# domains_router = routers.NestedSimpleRouter(router, r'domains', lookup='domain')
# Nested routers for Academic sessiion
academic_sessions_router = routers.NestedDefaultRouter(router, 'academic-sessions', lookup='academic_session')
academic_sessions_router.register('terms', views.TermViewSet, basename='academic-session-terms')

# Nested Router for Schools
school_router = routers.NestedDefaultRouter(router, 'schools', lookup='school')
school_router.register('classes', views.SchoolClassViewSet, basename='school-classes')


urlpatterns = [
  path('v1/', include(router.urls))
]
urlpatterns = urlpatterns + academic_sessions_router.urls + school_router.urls

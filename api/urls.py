from django.urls import path, include

from rest_framework.routers import DefaultRouter


from . import views


router = DefaultRouter()
router.register('schools', views.SchoolViewSet, basename='schools')



urlpatterns = [
  path('v1/', include(router.urls))
]
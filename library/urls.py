from django.urls import path
from .views import LibraryView

urlpatterns = [
  path('view-libary/', LibraryView.as_view(), name='library')
]
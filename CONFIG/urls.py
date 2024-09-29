from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from quiz.views import addQuestion

urlpatterns = [
    path('djangoadmin/', admin.site.urls),
    path('', include("main.urls")),
    path('library/', include("library.urls")),
    path('myquiz/', include("myquiz.urls")),
    path('report/', include('report.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

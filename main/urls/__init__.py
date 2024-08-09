from .teachers_url import urlpatterns as teachers_urlpatterns
from .admin_url import urlpatterns as admins_urlpatterns
from .student_urls import urlpatterns as students_urlpatterns
from .superadmin_url import urlpatterns as superadmins_urlpatterns

urlpatterns = teachers_urlpatterns + admins_urlpatterns + \
    students_urlpatterns + superadmins_urlpatterns

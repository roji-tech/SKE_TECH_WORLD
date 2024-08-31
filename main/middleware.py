from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class AppendSlashMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Ignore URLs that are explicitly marked with no-slash or already have a slash
        if request.path.endswith('/') or '.' in request.path.split('/')[-1]:
            return None

        # Check if the URL should end with a slash
        if settings.APPEND_SLASH and not request.path.endswith('/'):
            # Build the new URL with a slash appended
            new_url = f"{request.path}/"
            if request.GET:
                new_url += f"?{request.META['QUERY_STRING']}"
            return HttpResponsePermanentRedirect(new_url)
        
        return None

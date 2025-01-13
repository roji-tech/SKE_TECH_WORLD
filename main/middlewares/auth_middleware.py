from django.db.models import Q
from django.shortcuts import redirect
from main.models.models import School


class SchoolCodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path_parts = request.path.strip('/').split('/')

        try:
            if not len(path_parts) > 0:
                raise Exception("Invalid path: No path parts found")

            school_code = str(path_parts[0])
            print("School Code in Middleware: ", school_code)

            school = School.objects.filter(
                # Case-insensitive match
                Q(code__iexact=school_code) | Q(short_name__iexact=school_code)
            ).first()
            # if school and school.short_name and school.short_name is not None:
            #     # Redirect to short_name if code is used
            #     return redirect(f'/{school.short_name}/' + '/'.join(path_parts[1:]))

            if not school:
                raise School.DoesNotExist("School not found")

            request.school_code = school_code
            request.school = school
        except Exception as e:
            request.school_code = None
            request.school = None

        print("School Middleware: ", request.school_code, request.school)
        response = self.get_response(request)
        return response

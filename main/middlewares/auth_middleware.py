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
        
            school_code = str(path_parts[0]).upper()
            school = School.objects.filter(code=school_code).first()

            if school and school.short_name and school.short_name is not None:
                # Redirect to short_name if code is used
                return redirect(f'/{school.short_name}/' + '/'.join(path_parts[1:]))

            if not school:
                school = School.objects.filter(short_name=school_code).first()

            request.school_code = school_code
            request.school = school
        except Exception as e:
            request.school_code = None
            request.school = None

        print("School Code Middleware: ", request.school_code, request.school)
        response = self.get_response(request)
        return response

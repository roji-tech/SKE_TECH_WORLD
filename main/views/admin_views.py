from typing import Any
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import redirect, render
import django.utils.decorators
from django.views import View
from django.views.generic import ListView, CreateView
from django.contrib import messages

from main.models.users import OWNER, User
from main.models.models import AcademicSession, School
from django.contrib.auth import authenticate, login


def admin_is_authenticated(*args):
    print(args)
    return method_decorator(login_required(login_url="/admin/register/"), name='dispatch')


@admin_is_authenticated()
class AdminsHome(ListView):
    def get(self, request, *args, **kwargs):
        # Custom logic here
        return render(request, "myadmin/index.html")


class RegisterSchool(View):
    def get(self, request, *args, **kwargs):
        return render(request, "myadmin/register.html")

    def post(self, request, *args, **kwargs):
        print(request.POST)
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        school_name = request.POST.get('school_name')
        school_phone = request.POST.get('school_phone')
        school_email = request.POST.get('school_email')

        if all((first_name, last_name, email, password, gender)):
            try:
                owner = User(username=username, first_name=first_name, last_name=last_name,
                             email=email, gender=gender, role=OWNER)
                owner.set_password(password)
                owner.save()
                school = School(name=school_name, owner=owner,
                                phone=school_phone, email=school_email)
                school.save()

                messages.success(request, f"Account created successfuly.")
                return redirect('admin-login')

            except Exception as e:
                print(e)
                messages.error(
                    request, f"Error, please fill all fields correctly."
                )
        else:
            messages.error(
                request, f"Please fill all fields correctly."
            )

        return render(request, "myadmin/register.html")


class AdminLogin(View):
    def get(self, request, *args, **kwargs):
        return render(request, "myadmin/login.html")

    def post(self, request, *args, **kwargs):
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(user, username, password)

        if user is not None:
            print(user)
            login(request, user)
            return redirect('myadmin')
        else:
            messages.error(request, 'Invalid username or password')

        return render(request, "myadmin/login.html")


class AdminsHelp(View):
    def get(self, request, *args, **kwargs):
        # Custom logic here
        return render(request, "myadmin/help.html")


# ADMISSIN SESSION
@admin_is_authenticated()
class ListSession(ListView):
    template_name = "myadmin/list_session.html"

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        school = School.objects.filter(owner=user)
        return AcademicSession.objects.filter(school=school)

    # def get(self, request, *args, **kwargs):
    #     # Custom logic here
    #     return render(request, )

# ADMISSIN SESSION


@admin_is_authenticated()
class AddSession(View):
    template_name = "myadmin/add_session.html"

    def get(self, request, *args, **kwargs):
        # Custom logic here
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        start_date = request.POST.get('username')
        end_date = request.POST.get('password')
        next_session_begins = request.POST.get('password')
        is_current = request.POST.get('password')
        max_exam_score = request.POST.get('password')

        # if user is not None:
        #     print(user)
        #     login(request, user)
        #     return redirect('myadmin')
        # else:
        #     messages.error(request, 'Invalid username or password')

        return render(request, self.template_name)

from django.db import IntegrityError
from django.http.response import JsonResponse
from typing import Any
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from main.models.users import OWNER, User
from main.models.models import AcademicSession, School, Term, SchoolClass, Division
from django.contrib.auth import authenticate, login

# FORMS
from ..forms import AcademicSessionForm, ClassForm  # Assuming you have a form

# from ..models.profiles import Teacher
# from ..forms import TeachersForm


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
        print(username, first_name, last_name, email, password,
              gender, school_email, school_name, school_phone)

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
                return JsonResponse({
                    "status": True
                })

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

    def post(self, request, *args, **kwargs):
        try:
            # Extract POST data
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            gender = request.POST.get('gender')
            school_name = request.POST.get('school_name')
            school_phone = request.POST.get('school_phone')
            school_email = request.POST.get('school_email')

            # Log the extracted data for debugging
            print(
                f"""Received data: {username}, {first_name},
                {last_name}, {email}, {password}, {gender},
                {school_name}, {school_phone}, {school_email}"""
            )

            # Validate the received data
            if not all((username, first_name, last_name, email, password, gender, school_name, school_phone, school_email)):
                messages.error(request, "Please fill all fields correctly.")
                return JsonResponse({"status": False, "message": "Please fill all fields correctly."})

            # Create the User
            owner = User(username=username, first_name=first_name,
                         last_name=last_name, email=email, gender=gender, role=OWNER)
            owner.set_password(password)
            owner.save()

            # Create the School
            school = School(name=school_name, owner=owner,
                            phone=school_phone, email=school_email)
            school.save()

            # Success message
            messages.success(request, "Account created successfully.")
            return JsonResponse({"status": True, "message": "Account created successfully."})

        except Exception as e:
            # Log the exception
            print(f"Error creating account: {str(e)}")

            # Error message
            messages.error(
                request, "Error creating account. Please try again."
            )
            return JsonResponse({"status": False, "message": "Error creating account. Please try again."})


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


# ACADEMIC SESSION
# ACADEMIC SESSION
# ACADEMIC SESSION
@admin_is_authenticated()
class ListSession(ListView):
    template_name = "myadmin/list_sessions.html"
    context_object_name = 'academic_sessions'

    def get_queryset(self):
        return AcademicSession.get_school_sessions(request=self.request)


@admin_is_authenticated()
class AddSession(View):
    template_name = "myadmin/add_session.html"

    def get(self, request, *args, **kwargs):
        form = AcademicSessionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = AcademicSessionForm(request.POST)

        try:
            user = self.request.user
            school = School.objects.filter(owner=user).first()

            if form.is_valid():
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                _name = form.cleaned_data.get("name")
                school_name = _name if _name else f"{start_date.year}-{end_date.year}"
                print(start_date, end_date, _name, school_name, school)

                # is_current = form.cleaned_data.get('is_current')
                # next_session_begins = form.cleaned_data.get('next_session_begins')
                # max_exam_score = form.cleaned_data.get('max_exam_score')

                # Create and save the AcademicSession instance
                session = AcademicSession(
                    school_id=school.id,  # Adjust as needed
                    start_date=start_date,
                    end_date=end_date,
                    # is_current=is_current,
                    # next_session_begins=next_session_begins,
                    # max_exam_score=max_exam_score
                )
                session.save()

                messages.success(
                    request, 'Academic session added successfully!')
                # Redirect to a relevant page
                return redirect('/admin/sessions/')
            else:
                print(request.POST)
                print('Error adding academic session. Please try again.')

        # except School.DoesNotExist:
        #     messages.error(
        #         request, 'School not found. Please ensure your account is linked to a school.')
        except IntegrityError:
            messages.error(
                request, 'This academic session already exists. Please enter a different session.')
        except Exception as e:
            messages.error(
                request, 'Error adding academic session. Please try again.')
            print(e)

        form = AcademicSessionForm()
        return render(request, self.template_name, {'form': form})


class UpdateSession(UpdateView):
    model = AcademicSession
    context_object_name = 'academicSession'
    fields = ['start_date', 'end_date']
    template_name = "myadmin/update_session.html"
    success_url = reverse_lazy('list-sessions')

    def get_queryset(self):
        return AcademicSession.get_school_sessions(request=self.request)


class DeleteSession(DeleteView):
    model = AcademicSession
    template_name = "myadmin/delete_session.html"
    # Redirect after successful deletion
    success_url = reverse_lazy('list-sessions')

    def get_queryset(self):
        return AcademicSession.get_school_sessions(request=self.request)


# CLASSES
# CLASSES
# CLASSES
class ClassListView(ListView):
    model = SchoolClass
    template_name = 'myadmin/class/list.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return SchoolClass.get_school_classes(request=self.request)


class ClassDetailView(DetailView):
    model = SchoolClass
    template_name = 'myadmin/detail.html'
    context_object_name = 'class'

    def get_queryset(self):
        return SchoolClass.get_school_classes(request=self.request)


class ClassCreateView(CreateView):
    model = SchoolClass
    template_name = 'myadmin/class/add_class.html'
    form_class = ClassForm
    success_url = reverse_lazy('list-classes')

    def get_queryset(self):
        return SchoolClass.get_school_classes(request=self.request)

    # def get(self, request, *args, **kwargs):
    #     self.object = None
    #     context = self.get_context_data(**kwargs)
    #     # return render(request, self.template_name)
    #     kwargs.setdefault("content_type", self.content_type)
    #     return self.response_class(
    #         request=self.request,
    #         template=self.get_template_names(),
    #         context=context,
    #         using=self.template_engine,
    #         **kwargs,
    #     )

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)


class ClassUpdateView(UpdateView):
    model = SchoolClass
    template_name = 'myadmin/class/edit.html'
    # fields = ['name', 'academic_session', 'class_teacher', 'division']
    success_url = reverse_lazy('list-classes')
    form_class = ClassForm

    def get_queryset(self):
        return SchoolClass.get_school_classes(request=self.request)


class ClassDeleteView(DeleteView):
    model = SchoolClass
    template_name = 'myadmin/confirm_delete.html'
    success_url = reverse_lazy('list-classes')

    def get_queryset(self):
        return SchoolClass.get_school_classes(request=self.request)


# TERMS
# TERMS
# TERMS
class TermListView(ListView):
    model = Term
    template_name = 'myadmin/term_list.html'
    context_object_name = 'terms'


class TermDetailView(DetailView):
    model = Term
    template_name = 'myadmin/term_detail.html'
    context_object_name = 'term'


class TermCreateView(CreateView):
    model = Term
    template_name = 'myadmin/term_form.html'
    fields = ['academic_session', 'name',
              'start_date', 'end_date', 'next_term_begins']
    success_url = reverse_lazy('term-list')


class TermUpdateView(UpdateView):
    model = Term
    template_name = 'myadmin/term_form.html'
    fields = ['academic_session', 'name',
              'start_date', 'end_date', 'next_term_begins']
    success_url = reverse_lazy('term-list')


class TermDeleteView(DeleteView):
    model = Term
    template_name = 'myadmin/term_confirm_delete.html'
    success_url = reverse_lazy('term-list')


# CLASS DIVISIONS
# CLASS DIVISIONS
# CLASS DIVISIONS
class DivisionListView(ListView):
    model = Division
    template_name = 'myadmin/division_list.html'
    context_object_name = 'divisions'


class DivisionDetailView(DetailView):
    model = Division
    template_name = 'myadmin/division_detail.html'
    context_object_name = 'division'


class DivisionCreateView(CreateView):
    model = Division
    template_name = 'myadmin/division_form.html'
    fields = ['name']
    success_url = reverse_lazy('division-list')


class DivisionUpdateView(UpdateView):
    model = Division
    template_name = 'myadmin/division_form.html'
    fields = ['name']
    success_url = reverse_lazy('division-list')


class DivisionDeleteView(DeleteView):
    model = Division
    template_name = 'myadmin/division_confirm_delete.html'
    success_url = reverse_lazy('division-list')


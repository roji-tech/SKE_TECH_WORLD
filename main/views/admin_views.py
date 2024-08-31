from django.db.models import Q
import logging
from django.http import JsonResponse
from django.db import IntegrityError
from django.forms.models import BaseModelForm
from django.http.response import JsonResponse
from typing import Any
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from main.models import User, AcademicSession, School, SchoolSettings, Student, Subject, Teacher, Term, SchoolClass
from django.contrib.auth import authenticate, login

# FORMS
from main.models.models import School, Subject, Teacher
from main.forms import TeacherForm, UserForm, UserTeacherForm
from ..forms import AcademicSessionForm, ClassForm  # Assuming you have a form

# from ..models.profiles import Teacher
# from ..forms import TeachersForm


# Set up a logger for the application
logger = logging.getLogger(__name__)


def admin_is_authenticated(*args):
    # print(args)
    return method_decorator(login_required(login_url="/admin/login/"), name='dispatch')


@admin_is_authenticated()
class AdminsHome(ListView):
    def get(self, request, *args, **kwargs):
        # Custom logic here
        return render(request, "myadmin/index.html")


class RegisterAndRegisterSchool(View):
    def get(self, request, *args, **kwargs):
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

            # Validate the received data
            if not all([username, first_name, last_name, email, password, gender, school_name, school_phone, school_email]):
                messages.error(request, "Please fill all fields correctly.")
                return JsonResponse({"status": False, "message": "Please fill all fields correctly."})

            # Create the User
            owner = User(username=username, first_name=first_name,
                         last_name=last_name, email=email, gender=gender, role="owner")
            owner.set_password(password)
            owner.save()

            # Create the School
            school = School(name=school_name, owner=owner,
                            phone=school_phone, email=school_email)
            school.save()

            # Success message
            messages.success(request, "Account created successfully.")
            return JsonResponse({"status": True, "message": "Account created successfully."})

        except ValueError as ve:
            # Handle specific ValueErrors (e.g., invalid data types)
            logger.error(f"ValueError encountered: {str(ve)}")
            messages.error(request, "Invalid input provided.")
            return JsonResponse({"status": False, "message": "Invalid input provided."})

        except IntegrityError as ie:
            # Handle database integrity errors (e.g., unique constraint violations)
            logger.error(f"IntegrityError encountered: {str(ie)}")
            messages.error(
                request, "This username or email is already in use.")
            return JsonResponse({"status": False, "message": "This username or email is already in use."})

        except Exception as e:
            # Log the generic exception for further analysis
            logger.exception(f"Unexpected error occurred: {str(e)}")
            messages.error(
                request, "Error creating account. Please try again.")
            return JsonResponse({"status": False, "message": "Error creating account. Please try again."})


class AdminLogin(View):
    def get(self, request, *args, **kwargs):
        return render(request, "myadmin/login.html")

    def post(self, request, *args, **kwargs):
        try:
            # Extract POST data
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Log the login attempt
            logger.info(f"Login attempt for username: {username}")

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            logger.debug(f" Authenticated user: {user} for username: {username}")

            if user is not None:
                # If authentication is successful
                login(request, user)
                logger.info(f"User {username} logged in successfully.")
                return redirect('myadmin')
            else:
                # If authentication fails
                messages.error(request, 'Invalid username or password')
                logger.warning(
                    f"Failed login attempt for username: {username}")

        except Exception as e:
            # Log unexpected errors
            logger.exception(
                f'''Error occurred during login for username: {username}.
                Error: {str(e)}'''
            )
            messages.error(
                request, "An unexpected error occurred. Please try again later.")

        # If login fails or an error occurs, re-render the login page with an error message
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
                school_name = ""

                if _name:
                    school_name = _name
                else:
                    school_name = f"{start_date.year}-{end_date.year}"
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


@admin_is_authenticated()
class UpdateSession(UpdateView):
    model = AcademicSession
    context_object_name = 'academicSession'
    fields = ['start_date', 'end_date']
    template_name = "myadmin/update_session.html"
    success_url = reverse_lazy('list-sessions')

    def get_queryset(self):
        return AcademicSession.get_school_sessions(request=self.request)


@admin_is_authenticated()
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
# CLASSES
# CLASSES
@admin_is_authenticated()
class ClassListView(ListView):
    model = SchoolClass
    template_name = 'myadmin/class_list.html'
    context_object_name = 'classes'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(request=self.request, **self.get_form_kwargs())

    def get_queryset(self):
        return SchoolClass.get_school_classes(request=self.request)


@admin_is_authenticated()
class ClassDetailView(DetailView):
    model = SchoolClass
    template_name = 'myadmin/class_detail.html'
    context_object_name = 'class'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(request=self.request, **self.get_form_kwargs())

    def get_queryset(self):
        return SchoolClass.get_school_classes(request=self.request)


@admin_is_authenticated()
class ClassCreateView(CreateView):
    model = SchoolClass
    template_name = 'myadmin/class_create.html'
    form_class = ClassForm
    success_url = reverse_lazy('list-classes')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(request=self.request, **self.get_form_kwargs())

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


@admin_is_authenticated()
class ClassUpdateView(UpdateView):
    model = SchoolClass
    template_name = 'myadmin/class_edit.html'
    # fields = ['name', 'academic_session', 'class_teacher', 'division']
    success_url = reverse_lazy('list-classes')
    form_class = ClassForm

    def get_queryset(self):
        return SchoolClass.get_school_classes(request=self.request)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(request=self.request, **self.get_form_kwargs())


@admin_is_authenticated()
class ClassDeleteView(DeleteView):
    model = SchoolClass
    template_name = 'myadmin/class_delete.html'
    success_url = reverse_lazy('list-classes')

    def get_queryset(self):
        return SchoolClass.get_school_classes(request=self.request)


# TERMS
# TERMS
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


# SUBJECTS
# SUBJECTS
# SUBJECTS
# SUBJECTS
# SUBJECTS
# SUBJECTS
class SubjectListView(ListView):
    model = Subject
    template_name = 'myadmin/subject/subjects_list.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        queryset = Subject.get_school_subjects(request=self.request)
        class_id = self.request.GET.get('class_id')
        if class_id:
            queryset = queryset.filter(school_class_id=class_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the list of classes to the context
        context['school_classes'] = SchoolClass.get_school_classes(
            request=self.request)
        return context


class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'myadmin/subject/subject_detail.html'
    context_object_name = 'subject'

    def get_queryset(self):
        return Subject.get_school_subjects(request=self.request)


class SubjectCreateView(CreateView):
    model = Subject
    fields = ['name', 'school_class',]
    success_url = reverse_lazy('list-subjects')
    template_name = 'myadmin/subject/subject_create.html'

    def get_queryset(self):
        return Subject.get_school_subjects(request=self.request)

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data = request.POST
        school_class_id = data.get('school_class')
        subject_names = data.getlist('subject')
        print(data, school_class_id, subject_names)
        # print(dir(request.POST))

        # Get the SchoolClass instance
        school_class = SchoolClass.objects.get(id=school_class_id)

        # Create Subject instances
        for name in subject_names:
            if not Subject.objects.filter(school_class=school_class, name=name).exists():
                Subject.objects.create(school_class=school_class, name=name)

        return JsonResponse({'status': True, 'message': 'Subjects added successfully!'})


class SubjectUpdateView(UpdateView):
    model = Subject
    template_name = 'myadmin/subject/subject_edit.html'
    fields = ['name']
    success_url = reverse_lazy('list-subjects')

    # Adjust these fields according to your Subject model
    fields = ['name', 'school_class']
    context_object_name = 'subject'

    def get_queryset(self):
        return Subject.get_school_subjects(request=self.request)


class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'myadmin/subject/subject_delete.html'
    success_url = reverse_lazy('list-subjects')

    def get_queryset(self):
        return Subject.get_school_subjects(request=self.request)


# STUDENTS
# STUDENTS
# STUDENTS
# STUDENTS
# STUDENTS
# STUDENTS
class StudentListView(ListView):
    model = Student
    template_name = 'myadmin/student/students_list.html'
    context_object_name = 'students'


class StudentDetailView(DetailView):
    model = Student
    template_name = 'myadmin/student/student_detail.html'
    context_object_name = 'student'


class StudentCreateView(CreateView):
    model = Student
    template_name = 'myadmin/student/student_create.html'
    fields = ['name']
    success_url = reverse_lazy('list-subjects')

    def form_valid(self, form):
        user_form = UserForm(self.request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['user_form'] = UserForm()
        return context


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'myadmin/student/student_edit.html'
    fields = ['name']
    success_url = reverse_lazy('list-subjects')


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'myadmin/student/student_delete.html'
    success_url = reverse_lazy('list-subjects')


# TEACHERS
# TEACHERS
# TEACHERS
# TEACHERS
# TEACHERS
# TEACHERS
class TeacherListView(ListView):
    model = Teacher
    template_name = 'myadmin/teacher/teachers_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        queryset = Teacher.get_school_teachers(request=self.request)

        # Get search parameters
        search_query = self.request.GET.get('q', '')
        class_filter = self.request.GET.get('class', '')

        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(user__email__icontains=search_query) |
                Q(department__icontains=search_query) |
                Q(school_class__name__icontains=search_query)
            )

        if class_filter:
            # Assuming you have a relation between Teacher and Class
            # Adjust the filter according to your actual model relationships
            queryset = queryset.filter(
                subjects__school_class__name=class_filter
            )

        return queryset.distinct()


class TeacherDetailView(DetailView):
    model = User
    template_name = 'myadmin/teacher/teacher_detail.html'
    context_object_name = 'teacher'


class TeacherCreateView(CreateView):
    model = User
    template_name = 'myadmin/teacher/teacher_create.html'
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('list-teachers')
    form_class = TeacherForm

    def get(self, request, *args, **kwargs):
        user_form = UserTeacherForm()
        teacher_form = TeacherForm()
        return render(request, self.template_name, {'user_form': user_form, 'teacher_form': teacher_form})

    def post(self, request, *args, **kwargs):
        user_form = UserTeacherForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'teacher'
            user.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.school = School.get_user_school(request.user)
            teacher.save()
            messages.success(request, "Teacher created successfully!")
            return redirect('list-teachers')
        else:
            print(user_form.errors)
            print(teacher_form.errors)
            # messages.error(request, {"teacher":  "Error creating teacher."})
        return render(request, self.template_name, {'user_form': user_form, 'teacher_form': teacher_form})


class TeacherUpdateView(UpdateView):
    model = Teacher
    template_name = 'myadmin/teacher/teacher_create.html'
    form_class = UserTeacherForm
    success_url = reverse_lazy('list-teachers')

    def get(self, request, pk, *args, **kwargs):
        teacher = get_object_or_404(Teacher, pk=pk)
        user_form = UserTeacherForm(instance=teacher.user)
        teacher_form = TeacherForm(instance=teacher)
        return render(request, self.template_name, {'user_form': user_form, 'teacher_form': teacher_form, 'teacher': teacher})

    def post(self, request, pk, *args, **kwargs):
        teacher = get_object_or_404(Teacher, pk=pk)
        user_form = UserTeacherForm(request.POST, instance=teacher.user)
        teacher_form = TeacherForm(request.POST, instance=teacher)
        if user_form.is_valid() and teacher_form.is_valid():
            user_form.save()
            teacher_form.save()
            messages.success(request, "Teacher updated successfully!")
            return redirect('list-teachers')
        else:
            messages.error(request, "Error updating teacher.")
        return render(request, self.template_name, {'user_form': user_form, 'teacher_form': teacher_form, 'teacher': teacher})


class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'myadmin/teacher/teacher_delete.html'
    success_url = reverse_lazy('list-teachers')

    def post(self, request, pk, *args, **kwargs):
        teacher = get_object_or_404(Teacher, pk=pk)
        teacher.user.delete()
        teacher.delete()
        messages.success(request, "Teacher deleted successfully!")
        return redirect('list-teachers')

# SETTINGS
# SETTINGS
# SETTINGS
# SETTINGS
# SETTINGS
# SETTINGS


class SettingsListView(ListView):
    model = SchoolSettings
    template_name = 'myadmin/settings/settingss_list.html'
    context_object_name = 'settings'


class SettingsDetailView(DetailView):
    model = SchoolSettings
    template_name = 'myadmin/settings/settings_detail.html'
    context_object_name = 'setting'


class SettingsCreateView(CreateView):
    model = SchoolSettings
    template_name = 'myadmin/settings/settings_create.html'
    fields = ['name']
    success_url = reverse_lazy('list-settings')


class SettingsUpdateView(UpdateView):
    model = SchoolSettings
    template_name = 'myadmin/settings/settings_edit.html'
    fields = ['name']
    success_url = reverse_lazy('list-settings')


class SettingsDeleteView(DeleteView):
    model = SchoolSettings
    template_name = 'myadmin/settings/settings_delete.html'
    success_url = reverse_lazy('list-settings')

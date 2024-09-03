from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.core.exceptions import (
    NON_FIELD_ERRORS,
    FieldError,
    ImproperlyConfigured,
    ValidationError,
)

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ..models import User, STUDENT, TEACHER, SUPERADMIN, ADMIN, OWNER
# Custom Authentication Form


class CustomAuthenticationForm(AuthenticationForm):
    role = None
    username = forms.EmailField(
        label="Email", max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))

    def __init__(self, request=None, *args, **kwargs):
        if not self.role:
            self.role = kwargs.pop('role', None)

        if not self.role:
            raise ImproperlyConfigured(
                "The role kwargs must be supplied to CustomAuthenticationForm, The role attribute must be set in CustomLoginView or its subclasses."
            )

        super().__init__(*args, **kwargs)

    def confirm_login_allowed(self, user):
        user_role = user.role
        if user.role == OWNER:
            user_role = ADMIN

        print(user_role, self.role)
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.", code='inactive')

        if user_role != self.role or user_role == SUPERADMIN:
            raise forms.ValidationError(
                "Invalid login, Access Denied", code='access_denied')


class SuperAdminAuthenticationForm(CustomAuthenticationForm):
    role = SUPERADMIN

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.", code='inactive')

        if user.role != SUPERADMIN:
            raise forms.ValidationError(
                "Invalid login, Access Denied", code='access_denied')


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.htm'
    role = None
    page = None

    def __init__(self, *args, **kwargs):
        if not self.role:
            raise ImproperlyConfigured(
                "The role kwargs must be supplied to CustomLoginView."
            )

        if not self.page:
            raise ImproperlyConfigured(
                "The page attribute must be set in CustomLoginView or its subclasses. (e.g Teacher, Admin, Student )"
            )
        super().__init__(*args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(role=self.role, **self.get_form_kwargs())

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email or password.")
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user

        if user.is_owner or user.is_admin:
            return reverse_lazy('myadmin')
        elif user.is_teacher:
            return reverse_lazy('teachers')
        elif user.is_student:
            return reverse_lazy('students')
        else:
            return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page": self.page, })
        return context


class AdminLoginView(CustomLoginView):
    template_name = "myadmin/login.html"
    role = ADMIN
    page = "Admin"


class TeacherLoginView(CustomLoginView):
    page = "Teacher"
    template_name = "myadmin/login.html"
    role = TEACHER


class StudentLoginView(CustomLoginView):
    page = "Student"
    role = STUDENT
    ...


class SuperAdminLoginView(CustomLoginView):
    role = SUPERADMIN
    authentication_form = CustomAuthenticationForm
    template_name = 'login.htm'
    page = "Super Admin"

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email or password.")
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user

        if user.is_superadmin:
            return reverse_lazy('superadmin')
        else:
            return reverse_lazy('home')  # Fallback

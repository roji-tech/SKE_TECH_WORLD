from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView


class AdminHome(View):
    def get(self, request, *args, **kwargs):
        # Custom logic here
        return render(request, "Online School Management System/Teacher - Admin - Super Admin - Student/Admin/index.html")


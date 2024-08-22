from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from ..models.profiles import Teacher
from ..forms import TeachersForm


class AdminsHome(View):
    def get(self, request, *args, **kwargs):
        # Custom logic here
        return render(request, "myadmin/index.html")


def teachers_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'myadmins/employee/teachers List.html', {'teachers' : teachers})

def add_teacher(request):
    if request.method == 'POST':
        form = TeachersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teachers_list')
    return render(request, 'myadmins/employee/employeedata.html', {'form' : form})
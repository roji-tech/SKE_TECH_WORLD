from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from main.forms import GoogleMeetForm, LessonPlanForm
from main.models.models import GmeetClass, LessonPlan


class TeachersHome(View):
    def get(self, request, *args, **kwargs):
        # Custom logic here
        return render(request, "teachers/index.html")


"""LessonPlan Views"""


"""Notes Views"""


def add_notes(request):
    return render(request, "teachers/notes/TeachersNote.html")


def upload_notes(request):
    return render(request, "teachers/notes/uploadNote.html")


"""Examination Views"""


def view_examination(request):
    return render(request, "teachers/exam/examinations.html")


# """Assignments Views"""

# def continous_assessment_view(request):
#     if request.method == 'POST':
#         form = ContinuousAssessmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             assessment = form.save(commit=False)
#             assessment.uploaded_by = request.user.teacher
#             assessment.save()
#             return redirect('assessment-list')
#     else:
#         form = ContinuousAssessmentForm()

#     assessments = ContinuousAssessment.objects.filter(uploaded_by=request.user.teacher)

#     return render(request, 'teachers/homework/homework.html', {'form' : form, 'assessments': assessments})

# def edit_continous_assessnent(request, pk):
#     assessment = ContinuousAssessment.objects.get(uploaded_by=request.user.teacher, pk=pk)
#     if request.method == 'POST':
#         form = ContinuousAssessmentForm(request.POST, request.FILES, instance=assessment)
#         if form.is_valid():
#             form.save()
#             return redirect('assessment-list')
#     else:
#         form = ContinuousAssessmentForm()
#     return render(request, 'teachers/homework/homework.html', {'form' : form, 'assessment' : assessment})


def add_assignments(request):
    return render(request, "teachers/homework/homework.html")


"""results Views"""


def results_list(request):
    return render(request, "teachers/results/results.html")

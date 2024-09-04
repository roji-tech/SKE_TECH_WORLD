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


"""Google Meet Views"""


def add_gmeet(request):
    if request.method == "POST":
        form = GoogleMeetForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.created_by = request.user
            messages.success(request, 'Google Meet Session added successfully')
            return redirect('teachers')

    form = GoogleMeetForm()
    return render(request, 'teachers/gmeet/gmeet.html', {'form': form})


def teachers_edit_gmeet(request, pk):
    gmeets = get_object_or_404(GmeetClass, pk=pk)
    if request.method == "POST":
        form = GoogleMeetForm(request.POST, instance=gmeets)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Google Meet Session updated successfully')
            return redirect('teachers')

    form = GoogleMeetForm(instance=gmeets)
    return render(request, 'teachers/gmeet/uploadgmeet.html',  {'form': form, "gmeets": gmeets})


"""LessonPlan Views"""


def upload_lesson_plan(request, pk):
    lesson_plan = get_object_or_404(LessonPlan, pk=pk)
    if request.method == 'POST':

        form = LessonPlanForm(request.POST, request.FILES,
                              instance=lesson_plan)
        if form.is_valid():
            lesson_plan_instance = form.save(commit=False)
            lesson_plan_instance.uploaded_by = request.user
            lesson_plan_instance.save()
            return redirect('lessons_lists')
    else:

        form = LessonPlanForm(instance=lesson_plan)
        return render(request, 'teachers/lessonplan/edit-lesson-note.html', {'form': form, 'lesson_plan': lesson_plan})


def lessons_list(request):
    lesson_plans = LessonPlan.objects.all()
    return render(request, 'teachers/notes/lessonNoteList.html', {'lesson_plans': lesson_plans})


"""Notes Views"""


def add_notes(request):
    return render(request, 'teachers/notes/TeachersNote.html')


def upload_notes(request):
    return render(request, 'teachers/notes/uploadNote.html')


"""Examination Views"""


def view_examination(request):
    return render(request, 'teachers/exam/examinations.html')


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
    return render(request, 'teachers/homework/homework.html')


"""results Views"""


def results_list(request):
    return render(request, 'teachers/results/results.html')

from django.http import HttpResponse
from django.contrib import messages
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
            form.save()
            messages.success(request, 'Google Meet Session added successfully')
            return redirect('teachers')
    else:
        form = GoogleMeetForm()
    return render(request, 'teachers/gmeet/gmeet.html', {'form' : form})

def edit_gmeet(request, pk):
    gmeets = get_object_or_404(GmeetClass, pk=pk)
    if request.method == "POST":
        form = GoogleMeetForm(request.POST, instance=gmeets)
        if form.is_valid():
            form.save()
            messages.success(request, 'Google Meet Session updated successfully')
            return redirect('teachers')
        
    else:
        form = GoogleMeetForm(instance=gmeets)
    return render(request, 'teachers/gmeet/uploadgmeet.html',  {'form' : form, "gmeets" : gmeets})

"""LessonPlan Views"""
def upload_lesson_plan(request, pk):
    lesson_plan = get_object_or_404(LessonPlan, pk=pk)
    if request.method == "POST":
        form = LessonPlanForm(request.POST, instance=lesson_plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lesson plan updated successfully')
    return render(request, 'teachers/lessonplan/edit-lesson-note.html', {'form' : form, "lesson_plan" : lesson_plan})



def lessons_list(request):
    lesson_plans = LessonPlan.objects.all()
    return render(request, 'teachers/notes/lessonNoteList.html', {'lesson_plans' : lesson_plans})

"""Library"""
def library(request):
    return render(request, 'teachers/library/library.html')

"""Notes Views"""
def add_notes(request):
    return render(request, 'teachers/notes/TeachersNote.html')

def upload_notes(request):
    return render(request, 'teachers/notes/uploadNote.html')

"""Examination Views"""
def view_examination(request):
    return render(request, 'teachers/exam/examinations.html')

"""Assignments Views"""
def add_assignments(request):
    return render(request, 'teachers/homework/homework.html')


"""results Views"""
def results_list(request):
    return render(request, 'teachers/results/results.html')

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView


class TeachersHome(View):
    def get(self, request, *args, **kwargs):
        # Custom logic here
        return render(request, "teachers/index.html")

"""Google Meet Views"""
def addgmeet(request):
    return render(request, 'teachers/gmeet/gmeet.html')


def editgmeet(request):
    return render(request, 'teachers/gmeet/uploadgmeet.html' )

"""LessonPlan Views"""
def upload_lesson_plan(request):
    return render(request, 'teachers/lessonplan/edit-lesson-note.html')


def lessons_list(request):
    return render(request, 'teachers/notes/lessonNoteList.html')

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
    return render(request, 'teachers/results/results,html')

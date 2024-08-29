from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from ..models.models import ClassNote, GmeetClass

class StudentsHome(View):
    def get(self, request, *args, **kwargs):
        # Custom logic here
        return render(request, "students/index.html")
    
class StudentGoogleMeetListView(ListView):
    model = GmeetClass  
    template_name = 'students/inner/students-gmeet-list.html'
    context_object_name = 'gmeets'

    # def get_queryset(self, request):
    #     return GmeetClass.objects.filter(student=self.request.user.student)
    
class StudentClassNoteListView(ListView):
    model = ClassNote
    template_name = 'students/inner/students-class-note.html'
    context_object_name = 'notes'

    # def get_queryset(self, request):
    #     student = request.user.student
    #     return ClassNote.objects.filter(student=student)
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from ..models.models import ClassNote, GmeetClass



# class StudentsLogin(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, "teachers/students-login.html")

#     def post(self, request, *args, **kwargs):
#         print(request.POST)
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)
#         print(user, username, password)

#         if user is not None:
#             print(user)
#             login(request, user)
#             return redirect('myadmin')
#         else:
#             messages.error(request, 'Invalid username or password')

#         return render(request, "myadmin/login.html")

class StudentsHome(View):
    def get(self, request, *args, **kwargs):
        # Custom logic here
        return render(request, "students/index.html")
    
class StudentGoogleMeetListView(ListView):
    model = GmeetClass  
    template_name = 'students/inner/students-gmeet-list.html'
    context_object_name = 'gmeets'

    
class StudentClassNoteListView(ListView):
    model = ClassNote
    template_name = 'students/inner/students-class-note.html'
    context_object_name = 'notes'


def e_exam(request):
    return render(request, 'students/inner/e-exam.html') 


def exam_quiz(request):
    return render(request, 'students/inner/exam.html') 

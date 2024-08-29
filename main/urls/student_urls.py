from django.urls import path

from ..views import StudentsHome
from ..views.teacher_views import library

from main.views.student_views import StudentClassNoteListView, StudentGoogleMeetListView


urlpatterns = [
    path('students/', StudentsHome.as_view(), name='students_home'),

    path('view-library/', library, name='library'),

    path('view-google-classes/', StudentGoogleMeetListView.as_view(), name='google_meets_classes'),

    path('total-students/', StudentsHome.as_view(), name='total_students'),

    path('student/subjects/combination', StudentsHome.as_view(), name='student_subject_combination'),

    path('students/class-notes/', StudentClassNoteListView.as_view(), name='students_class_notes'),
]
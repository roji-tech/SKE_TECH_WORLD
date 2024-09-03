from django.urls import path

from ..views import StudentsHome

from main.views.student_views import StudentClassNoteListView, StudentGoogleMeetListView


urlpatterns = [
    path('students/', StudentsHome.as_view(), name='students'),

    # path('student/view-library/', library, name='library'),

    # path('student/take-exam/', e_exam, name='e-exam'),
    # path('student/take-exam/quiz/', exam_quiz, name='quiz-exam'),

    path('students/view-google-classes/', StudentGoogleMeetListView.as_view(), name='google_meets_classes'),

    path('total-students/', StudentsHome.as_view(), name='total_students'),

    path('student/subjects/combination', StudentsHome.as_view(), name='student_subject_combination'),

    path('students/class-notes/', StudentClassNoteListView.as_view(), name='students_class_notes'),
]
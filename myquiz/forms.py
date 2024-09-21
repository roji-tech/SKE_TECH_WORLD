

from django import forms
from .models import Quiz, Question, AcademicSession, Term
from main.models import School

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'quiz_type', 'school_class', 'subject', 'start_date', 'end_date', 'term']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Get the current user's school
        school = School.get_user_school(request.user)

        if school:
            # Get the current academic session for the school
            current_session = AcademicSession.objects.filter(school=school, is_current=True).first()

            if current_session:
                # Get the current term in the current session
                current_term = Term.objects.filter(academic_session=current_session).order_by('-start_date').first()

                # Set the current term as the default value for the 'term' field
                if current_term:
                    self.fields['term'].initial = current_term

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'image', 'option_1',
                  'option_2', 'option_3', 'option_4', 'correct_answer']

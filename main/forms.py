# from .models.profiles import Teacher


# class TeachersForm(forms.ModelForm):
#   email = forms.EmailField()

#   class Meta:
#     model = Teacher
#     fields =  ['name', 'email', 'gender', 'department', 'subjects', 'pictures', 'specifications']
#     widgets = {
#       'gender' : forms.Select(),
#       "department" : forms.Select(),
#       'specifications' : forms.Textarea(attrs={'rows' : 4})
#     }


from django import forms

from main.models.models import ContinuousAssessment, GmeetClass, LessonPlan, SchoolClass
from .models import AcademicSession


class AcademicSessionForm(forms.ModelForm):
    class Meta:
        model = AcademicSession
        fields = [
            'start_date',
            'end_date',
            "name",
            # 'is_current', 'next_session_begins', 'max_exam_score'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', "id": "start_date"}),
            'end_date': forms.DateInput(attrs={'type': 'date', "id": "end_date"}),
            'name': forms.TextInput(attrs={'type': 'text', "id": "name", "placeholder": "2024-2025 ( optional )"}),
            # 'next_session_begins': forms.DateInput(attrs={'type': 'date'}),
        }


class ClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ['name', 'academic_session',
                  'class_teacher', 'division', 'category']

    def __init__(self, *args, **kwargs):
        # Extract the request object from the keyword arguments
        self.request = kwargs.pop('request', None)
        super(ClassForm, self).__init__(*args, **kwargs)

        self.fields['academic_session'].queryset = AcademicSession.get_school_sessions(
            self.request)

        if self.request:
            self.fields['academic_session'].queryset = AcademicSession.get_school_sessions(
                self.request)

        # widgets = {SchoolClass
        #     'start_date': forms.DateInput(attrs={'type': 'date', "id": "start_date"}),
        #     'end_date': forms.DateInput(attrs={'type': 'date', "id": "end_date"}),
        #     'name': forms.TextInput(attrs={'type': 'text', "id": "name", "placeholder": "2024-2025 ( optional )"}),
        #     # 'next_session_begins': forms.DateInput(attrs={'type': 'date'}),
        # }

class GoogleMeetForm(forms.ModelForm):
    class Meta:
        model = GmeetClass
        fields = ['subject', 'description', 'start_time', 'gmeet_link', 'created_by']
        widgets = {
        'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    }
        labels = {
            'subject': 'Meeting Title',
            'start_time': 'Date and Time',
            'created_by': 'Created By',
        }

class LessonPlanForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = ['id', 'school_class', 'subject', 'uploaded_by', 'uploaded_file']
        widgets = {
                'uploaded_file': forms.ClearableFileInput(attrs={'class': 'input'}),
                'school_class': forms.Select(attrs={'class': 'input'}),
            }
    
class ContinuousAssessmentForm(forms.ModelForm):
    class Meta:
        model = ContinuousAssessment
        fields = ['subject', 'file', 'student', 'name', 'score']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
        }

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if not (0 <= score <= 100):
            raise forms.ValidationError("Score must be between 0 and 100.")
        return score
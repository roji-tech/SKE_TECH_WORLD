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

from main.models.models import SchoolClass
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

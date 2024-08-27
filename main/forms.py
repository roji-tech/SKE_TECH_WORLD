from .models import AcademicSession
from main.models.models import SchoolClass
from django import forms

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


class CustomSelect(forms.widgets.Select):
    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs, choices)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option_dict = super().create_option(name, value, label, selected,
                                            index, subindex=subindex, attrs=attrs)
        # Customize the `option` elements
        option_dict['attrs']['class'] = 'custom-option-class'
        # Example of inline styles for options
        option_dict['attrs']['style'] = 'color: blue;'
        return option_dict


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

        widgets = {
            'school_class': CustomSelect(attrs={
                'class': 'custom-select-class',  # Add your custom class
                'style': 'background-color: #f5f5f5; color: #333;',  # Custom inline styles
                'data-custom-attribute': 'example',  # Add custom data attributes if needed
            }),
        }


class GoogleMeetForm(forms.ModelForm):
    class Meta:
        model = GmeetClass
        fields = ['subject', 'description',
                  'start_time', 'gmeet_link', 'created_by']
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
        fields = ['id', 'school_class', 'subject',
                  'uploaded_by', 'uploaded_file']
        widgets = {
            'uploaded_file': forms.ClearableFileInput(attrs={'class': 'input'}),
            'school_class': forms.Select(attrs={'class': 'input'}),
        }

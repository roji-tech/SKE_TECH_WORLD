from django import forms
from library.models import LibraryBook
from main.models.models import (
    AcademicSession, SchoolClass,
    GmeetClass, LessonPlan, Subject,
    User, Teacher, Student
)


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['department']

        widgets = {
            'department': forms.TextInput(attrs={
                'placeholder': 'Enter Department',
                'class': 'input',
                'required': 'required'
            }),
        }


class TeacherUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'gender', 'email', "phone"]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter Name',
                'class': 'input',
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter Name',
                'class': 'input',
                'required': 'required'
            }),
            'gender': forms.Select(attrs={
                'class': 'input-1',
                'required': 'required'
            }, choices=[('', 'Select Gender'), ('M', 'Male'), ('F', 'Female')]),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter Email',
                'class': 'input',
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter Email',
                'class': 'input',
            }),
            # 'image': forms.ClearableFileInput(attrs={
            #     'onchange': 'previewImage(this);'
            # })
        }

    password = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Password',
            'class': 'input',
            'disabled': 'disabled',
            'value': "Disabled: Teacher's Surname in lowercase is default"
        }),
        required=False
    )


class StudentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # Extract the request object from the keyword arguments
        self.request = kwargs.pop('request', None)
        super(StudentForm, self).__init__(*args, **kwargs)

        print(self.fields)
        if self.request:
            self.fields['academic_year'].queryset = AcademicSession.get_school_sessions(
                self.request)

    class Meta:
        model = Student
        fields = [
            'date_of_birth',
            'admission_date',
            'student_class',
            'academic_year',
            'reg_no'
        ]
        widgets = {
            # 'student_id': forms.TextInput(attrs={
            #     'placeholder': 'Enter Student ID',
            #     'class': 'input',
            #     'required': 'required'
            # }),
            'date_of_birth': forms.DateInput(attrs={
                'placeholder': 'YYYY-MM-DD',
                'class': 'input',
                'required': 'required',
                'type': 'date'
            }),
            'admission_date': forms.DateInput(attrs={
                'placeholder': 'YYYY-MM-DD',
                'class': 'input',
                'required': 'required',
                'type': 'date'
            }),
            'student_class': forms.Select(attrs={
                'class': 'input-1',
                'required': 'required'
            }),
            'academic_year': forms.Select(attrs={
                'class': 'input-1',
                'required': 'required'
            }),
            'reg_no': forms.TextInput(attrs={
                'placeholder': 'Enter Registration Number',
                'class': 'input',
                'required': 'required'
            }),
        }


class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter Name',
                'class': 'input',
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter Name',
                'class': 'input',
                'required': 'required'
            }),
            'gender': forms.Select(attrs={
                'class': 'input-1',
                'required': 'required'
            }, choices=[('', 'Select Gender'), ('M', 'Male'), ('F', 'Female')]),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter Email',
                'class': 'input',
            }),
            # 'image': forms.ClearableFileInput(attrs={
            #     'onchange': 'previewImage(this);'
            # })
        }

    password = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Password',
            'class': 'input',
            'disabled': 'disabled',
            'value': "Disabled: Student's Surname in lowercase is default"
        }),
        required=False
    )


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
        widgets = {
            'school_class': CustomSelect(attrs={
                'class': 'custom-select-class',  # Add your custom class
                'style': 'background-color: #f5f5f5; color: #333;',  # Custom inline styles
                'data-custom-attribute': 'example',  # Add custom data attributes if needed
            }),
        }

    def __init__(self, *args, **kwargs):
        # Extract the request object from the keyword arguments
        self.request = kwargs.pop('request', None)
        super(ClassForm, self).__init__(*args, **kwargs)

        if self.request:
            print(
                Teacher.objects.filter(
                    school__in=AcademicSession.get_school_sessions(
                        self.request
                    ).values('school')
                )
            )
            self.fields['academic_session'].queryset = AcademicSession.get_school_sessions(
                self.request
            )
            self.fields['class_teacher'].queryset = Teacher.objects.filter(
                school__in=AcademicSession.get_school_sessions(
                    self.request
                ).values('school')
            )

    def clean(self):
        self._validate_unique = True
        print("""
        
        
        hello
        
        """)
        print(self.cleaned_data)
        return self.cleaned_data

    


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['school_class', 'name']
        widgets = {
            'school_class': forms.Select(attrs={'class': 'input', 'placeholder': 'Select'}),
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter Subject Name'}),
        }


class GoogleMeetForm(forms.ModelForm):
    class Meta:
        model = GmeetClass
        fields = ['subject', 'description',
                  'start_time', 'gmeet_link']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            # 'subject': 'Meeting Title',
            'start_time': 'Date and Time',
        }


class LessonPlanForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = ['id', 'school_class', 'subject',
                  'uploaded_by', 'uploaded_file']
        widgets = {
            'uploaded_file': forms.ClearableFileInput(attrs={'class': 'input'}),
            'school_clas': forms.Select(attrs={'class': 'input'}),
        }


class LibraryBookForm(forms.ModelForm):
    class Meta:
        model = LibraryBook
        fields = '__all__'




# class ContinuousAssessmentForm(forms.ModelForm):
#     class Meta:
#         model = ContinuousAssessment
#         fields = ['subject', 'file', 'student', 'name', 'score']
#         widgets = {
#             'subject': forms.Select(attrs={'class': 'form-control'}),
#             'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
#             'student': forms.Select(attrs={'class': 'form-control'}),
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
#         }

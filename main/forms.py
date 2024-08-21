from django import forms
from .models.models import *
from .models.profiles import Teacher


class TeachersForm(forms.ModelForm):
  class Meta:
    model = Teacher 
    fields =  ['']
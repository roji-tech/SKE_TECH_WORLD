from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.shortcuts import render

# Create your views here.


from django import forms
from main import mydecorators
from .models import Complaint


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'description']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Enter complaint subject'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the issue'}),
        }


@mydecorators.admin_is_authenticated
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user  # Associate complaint with the logged-in admin
            complaint.save()
            return redirect('complaints')
    else:
        form = ComplaintForm()
    return render(request, 'report/submit_complaint.html', {'form': form})

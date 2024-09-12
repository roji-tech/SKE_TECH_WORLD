from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from main.models.models import GmeetClass, Subject

from django import forms


class GmeetClassForm(forms.ModelForm):  # GmeetClass Form
    class Meta:
        model = GmeetClass
        fields = ["title", 'subject', 'description',
                  'gmeet_link', 'start_time', 'duration']
        widgets = {
            'title': forms.TextInput(attrs={'type': 'text', 'class': 'input', 'required': 'false', 'id': "meeting-title", 'placeholder': "Meeting Title"}),
            'subject': forms.Select(attrs={'class': 'input'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input', 'required': 'true'}),
            'duration': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Duration in minutes', 'required': 'true', 'min': 0}),            'gmeet_link': forms.URLInput(attrs={'class': 'input', 'placeholder': 'Link'}),
            'description': forms.Textarea(attrs={'class': 'input', 'placeholder': 'Description', 'required': 'false', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pop user from kwargs
        super(GmeetClassForm, self).__init__(*args, **kwargs)

        if user and user.role == "teacher":
            # Filter subjects based on the logged-in teacher
            self.fields['subject'].queryset = Subject.objects.filter(
                teacher=user)
        else:
            # Show all subjects for admins or other users
            self.fields['subject'].queryset = Subject.objects.all()

# Gmeet Classes
# Gmeet Classes
# Gmeet Classes
# Gmeet Classes
# Gmeet Classes
# Gmeet Classes


class ClassFormView:
    def form_valid(self, form):
        # Set the created_by field to the logged-in user
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs


class GmeetClassListView(ListView):  # GmeetClass ListView
    model = GmeetClass
    template_name = 'gmeet/gmeet_list.html'
    context_object_name = 'gmeet_classes'

    def get_queryset(self):  # Filter the Gmeet classes based on the school or user criteria
        qs = GmeetClass.filter_by_role(self.request)
        print(qs)
        return qs


class GmeetClassDetailView(DetailView):  # GmeetClass DetailView
    model = GmeetClass
    template_name = 'gmeetclass_detail.html'
    context_object_name = 'gmeet_class'


class GmeetClassCreateView(CreateView, ClassFormView):  # GmeetClass Create View
    model = GmeetClass
    form_class = GmeetClassForm
    template_name = 'gmeet/gmeet_create.html'
    success_url = reverse_lazy('gmeetclass-list')


class GmeetClassUpdateView(UpdateView, ClassFormView):  # GmeetClass Update View
    model = GmeetClass
    form_class = GmeetClassForm
    template_name = 'gmeet/gmeet_create.html'
    success_url = reverse_lazy('gmeetclass-list')


class GmeetClassDeleteView(DeleteView):  # GmeetClass Delete View
    model = GmeetClass
    template_name = 'gmeet/gmeetclass_confirm_delete.html'
    success_url = reverse_lazy('gmeetclass-list')

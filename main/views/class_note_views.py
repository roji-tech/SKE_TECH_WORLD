# from .views import (
#     GmeetClassListView, GmeetClassDetailView, GmeetClassCreateView, GmeetClassUpdateView, GmeetClassDeleteView,
#     LessonPlanListView, LessonPlanDetailView, LessonPlanCreateView, LessonPlanUpdateView, LessonPlanDeleteView,
#     ClassNoteListView, ClassNoteDetailView, ClassNoteCreateView, ClassNoteUpdateView, ClassNoteDeleteView
# )
from django.views.generic import ListView, DetailView
# from .forms import GmeetClassForm, LessonPlanForm, ClassNoteForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from main.models.models import GmeetClass, School, LessonPlan, ClassNote

from django import forms


class ClassNoteForm(forms.ModelForm):  # ClassNote Form
    class Meta:
        model = ClassNote
        fields = ['lesson_plan', 'title', 'content', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'attachment': forms.URLInput(attrs={'placeholder': 'Attach a link to the file'})
        }


class ClassNoteCreateView(CreateView):  # ClassNote Create View
    model = ClassNote
    form_class = ClassNoteForm
    template_name = 'classnote_form.html'
    success_url = reverse_lazy('classnote-list')


class ClassNoteUpdateView(UpdateView):  # ClassNote Update View
    model = ClassNote
    form_class = ClassNoteForm
    template_name = 'classnote_form.html'
    success_url = reverse_lazy('classnote-list')


class ClassNoteDeleteView(DeleteView):  # ClassNote Delete View
    model = ClassNote
    template_name = 'classnote_confirm_delete.html'
    success_url = reverse_lazy('classnote-list')


class ClassNoteListView(ListView):  # ClassNote ListView
    model = ClassNote
    template_name = 'classnote_list.html'
    context_object_name = 'class_notes'

    def get_queryset(self):
        # Filter class notes by school
        return ClassNote.objects.filter(school_class__school=self.request.user.school)


class ClassNoteDetailView(DetailView):  # ClassNote DetailView
    model = ClassNote
    template_name = 'classnote_detail.html'
    context_object_name = 'class_note'


class ClassNoteListView(ListView):  # ClassNote ListView with filters
    model = ClassNote
    template_name = 'notes/notes.html'
    context_object_name = 'class_notes'

    def get_queryset(self):  # Assuming class is passed as a GET param
        school_class = self.request.GET.get('class')
        return ClassNote.filter_by_class(school_class)

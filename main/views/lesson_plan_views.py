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



class LessonPlanForm(forms.ModelForm):  # LessonPlan Form
    class Meta:
        model = LessonPlan
        fields = ['school_class', 'subject', 'uploaded_file']
        widgets = {
            'uploaded_file': forms.ClearableFileInput(attrs={'accept': 'application/pdf,application/msword'})
        }


class ClassNoteForm(forms.ModelForm):  # ClassNote Form
    class Meta:
        model = ClassNote
        fields = ['lesson_plan', 'title', 'content', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'attachment': forms.URLInput(attrs={'placeholder': 'Attach a link to the file'})
        }


class LessonPlanCreateView(CreateView):  # LessonPlan Create View
    model = LessonPlan
    form_class = LessonPlanForm
    template_name = 'lessonplan_form.html'
    success_url = reverse_lazy('lessonplan-list')

    def form_valid(self, form):
        # Set the uploader as the current user
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)


class LessonPlanUpdateView(UpdateView):  # LessonPlan Update View
    model = LessonPlan
    form_class = LessonPlanForm
    template_name = 'lessonplan_form.html'
    success_url = reverse_lazy('lessonplan-list')


class LessonPlanDeleteView(DeleteView):  # LessonPlan Delete View
    model = LessonPlan
    template_name = 'lessonplan_confirm_delete.html'
    success_url = reverse_lazy('lessonplan-list')


class AdminLessonPlanListView(ListView):  # LessonPlan ListView
    model = LessonPlan
    template_name = 'lessonplan_list.html'
    context_object_name = 'lesson_plans'

    def get_queryset(self):
        school = School.get_user_school(self.request.user)
        return LessonPlan.filter_by_school(school)


class TeachersLessonPlanListView(ListView):  # LessonPlan ListView with filters
    model = LessonPlan
    template_name = 'lesson_plan_list.html'
    context_object_name = 'lesson_plans'

    def get_queryset(self):
        school = School.get_user_school(self.request.user)
        return LessonPlan.filter_by_school(school)


class LessonPlanListView(ListView):  # LessonPlan ListView with filters
    model = LessonPlan
    template_name = 'lesson_plan_list.html'
    context_object_name = 'lesson_plans'

    def get_queryset(self):
        school = School.get_user_school(self.request.user)
        return LessonPlan.filter_by_school(school)


class LessonPlanDetailView(DetailView):  # LessonPlan DetailView
    model = LessonPlan
    template_name = 'lessonplan_detail.html'
    context_object_name = 'lesson_plan'


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
    template_name = 'class_note_list.html'
    context_object_name = 'class_notes'

    def get_queryset(self):  # Assuming class is passed as a GET param
        school_class = self.request.GET.get('class')
        return ClassNote.filter_by_class(school_class)


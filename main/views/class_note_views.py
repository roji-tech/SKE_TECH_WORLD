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

# ClassNote Form
class ClassNoteForm(forms.ModelForm):
    class Meta:
        model = ClassNote
        fields = ['lesson_plan', 'title', 'content', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'attachment': forms.URLInput(attrs={'placeholder': 'Attach a link to the file'})
        }


# ClassNote Create View
class ClassNoteCreateView(CreateView):
    model = ClassNote
    form_class = ClassNoteForm
    template_name = 'classnote_form.html'
    success_url = reverse_lazy('classnote-list')


# ClassNote Update View
class ClassNoteUpdateView(UpdateView):
    model = ClassNote
    form_class = ClassNoteForm
    template_name = 'classnote_form.html'
    success_url = reverse_lazy('classnote-list')


# ClassNote Delete View
class ClassNoteDeleteView(DeleteView):
    model = ClassNote
    template_name = 'classnote_confirm_delete.html'
    success_url = reverse_lazy('classnote-list')


# Consolidated ClassNote List View with optional filtering
class ClassNoteListView(ListView):
    model = ClassNote
    template_name = 'notes/notes.html'
    context_object_name = 'class_notes'

    def get_queryset(self):
        """
        If 'class' is provided as a GET parameter, filter by class;
        otherwise, filter by the school of the logged-in user.
        """
        school_class = self.request.GET.get('class')
        if school_class:
            return ClassNote.filter_by_class(school_class)
        return ClassNote.objects.filter(school_class__school=self.request.user.school)


# ClassNote Detail View
class ClassNoteDetailView(DetailView):
    model = ClassNote
    template_name = 'classnote_detail.html'
    context_object_name = 'class_note'



# def upload_lesson_plan(request, pk):
#     lesson_plan = get_object_or_404(LessonPlan, pk=pk)
#     if request.method == "POST":

#         form = LessonPlanForm(request.POST, request.FILES,
#                               instance=lesson_plan)
#         if form.is_valid():
#             lesson_plan_instance = form.save(commit=False)
#             lesson_plan_instance.uploaded_by = request.user
#             lesson_plan_instance.save()
#             return redirect("lessons_lists")

#     else:

#         form = LessonPlanForm(instance=lesson_plan)
#         return render(
#             request,
#             "teachers/lessonplan/edit-lesson-note.html",
#             {"form": form, "lesson_plan": lesson_plan},
#         )


# def lessons_list(request):
#     lesson_plans = LessonPlan.objects.all()
#     return render(
#         request, "teachers/notes/lessonNoteList.html", {
#             "lesson_plans": lesson_plans}
#     )

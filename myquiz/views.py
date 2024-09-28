from django.forms import modelformset_factory
import django.forms
from .forms import QuestionFormSet
from .models import Question
from django.contrib import messages
from django.utils import timezone
from .models import Quiz, Question
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from main import mydecorators
from .models import Quiz, Question, Result

from django.shortcuts import render, redirect
from .forms import QuizForm, QuestionForm
from .models import Quiz, Question, QuestionBank


from django.views.generic import DetailView


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'
    context_object_name = 'quiz'


@mydecorators.teacher_is_authenticated
def create_quiz(request):
    if request.method == "POST":
        quiz_form = QuizForm(request.POST, request=request)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            # Assuming Teacher has a relation to User
            quiz.created_by = request.user
            quiz.save()
            return redirect('add-question', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm(request=request)

    return render(request, 'quiz/quiz_form.html', {'form': quiz_form})


@mydecorators.teacher_is_authenticated
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Initialize the formset, allowing up to 5 questions to be added at once
    QuestionFormSet = modelformset_factory(
        Question, form=QuestionForm, extra=5, can_delete=True)

    if request.method == 'POST':
        formset = QuestionFormSet(
            request.POST, request.FILES, queryset=Question.objects.none())
        if formset.is_valid():
            # Save each form in the formset, linking it to the specific quiz
            instances = formset.save(commit=False)
            for instance in instances:
                instance.quiz = quiz
                instance.save()
            messages.success(request, 'Questions added successfully!')
            # Redirect to quiz detail view or any desired page
            return redirect('quiz_detail', pk=quiz.id)
        else:
            print(formset.errors)
            messages.error(
                request, 'There was an error adding the questions. Please try again.')
    else:
        formset = QuestionFormSet(queryset=Question.objects.none())

    return render(request,  'quiz/add_questions.html',  {
        'quiz': quiz,
        'formset': formset,
    })


# @mydecorators.teacher_is_authenticated
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        correct_answers = 0
        total_questions = questions.count()

        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option == question.correct_option:
                correct_answers += 1

        # Calculate the score
        score = (correct_answers / total_questions) * 100

        # Save the result for the student
        Result.objects.create(
            student=request.user.student,  # Assuming the student is related to the user
            quiz=quiz,
            score=score,
            term=quiz.term,
            session="2023-2024"  # Replace with actual session logic
        )

        return redirect('quiz_result', score=score)

    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions': questions})


# @mydecorators.teacher_is_authenticated
def quiz_result(request, score):
    """
    View to display the quiz result after a student completes a quiz.
    """
    return render(request, 'quiz/quiz_result.html', {'score': score})

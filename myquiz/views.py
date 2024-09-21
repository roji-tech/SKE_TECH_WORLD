from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from .models import Quiz, Question, Result

from django.shortcuts import render, redirect
from .forms import QuizForm, QuestionForm
from .models import Quiz, Question, QuestionBank


def create_quiz(request):
    if request.method == "POST":
        quiz_form = QuizForm(request.POST, request=request)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            # Assuming Teacher has a relation to User
            quiz.created_by = request.user.teacher
            quiz.save()
            return redirect('add-question', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm(request=request)

    return render(request, 'quiz/quiz_form.html', {'form': quiz_form})


def add_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == "POST":
        question_form = QuestionForm(request.POST, request.FILES)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            # Add question to the question bank
            QuestionBank.objects.create(
                subject=quiz.subject, question=question)
            return redirect('add-question', quiz_id=quiz.id)
    else:
        question_form = QuestionForm()

    return render(request, 'quiz/add_question.html', {'question_form': question_form, 'quiz': quiz})


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


# views.py
def quiz_result(request, score):
    """
    View to display the quiz result after a student completes a quiz.
    """
    return render(request, 'quiz/quiz_result.html', {'score': score})

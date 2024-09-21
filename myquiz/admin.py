from django.contrib import admin
from myquiz.admin_filters import AcademicSessionFilter
from .models import Quiz, Question, QuestionBank, StudentAnswer, Result, TermResult, SessionResult


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of extra blank question fields


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'quiz_type', 'school_class', 'subject',
                    'term', 'academic_session', 'created_by', 'start_date', 'end_date')
    list_filter = ('quiz_type', 'school_class', 'subject', 'term', AcademicSessionFilter)
    search_fields = ('title', 'school_class__name', 'subject__name')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_text', 'correct_answer')
    list_filter = ('quiz', 'quiz__school_class', 'quiz__subject')
    search_fields = ('question_text', 'quiz__title')


@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('subject', 'question_text')
    search_fields = ('question_text', 'subject__name')


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'selected_option')
    list_filter = ('question__quiz', 'student')
    search_fields = ('student__name', 'question__question_text')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score')
    list_filter = ('quiz', 'student')
    search_fields = ('student__name', 'quiz__title')


@admin.register(TermResult)
class TermResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'school_class', 'term',
                    'academic_session', 'total_score')
    list_filter = ('school_class', 'term', 'academic_session')
    search_fields = ('student__name', 'school_class__name')


@admin.register(SessionResult)
class SessionResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'school_class',
                    'academic_session', 'total_score')
    list_filter = ('school_class', 'academic_session')
    search_fields = ('student__name', 'school_class__name')

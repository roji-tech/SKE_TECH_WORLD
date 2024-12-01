# File: school_management/models.py
from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)

    def __str__(self):
        return self.name


class AcademicSession(models.Model):
    session_name = models.CharField(max_length=20)  # e.g., "2023/2024"
    start_date = models.DateField()
    end_date = models.DateField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.session_name


class Term(models.Model):
    TERM_CHOICES = [
        ('1', 'Term 1'),
        ('2', 'Term 2'),
        ('3', 'Term 3'),
    ]
    term = models.CharField(max_length=1, choices=TERM_CHOICES)
    academic_session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.term} - {self.academic_session.session_name}"


class SchoolClass(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Grade 1", "Primary 2"
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Staff(models.Model):
    ROLE_CHOICES = [
        ('T', 'Teaching'),
        ('NT', 'Non-Teaching'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    hire_date = models.DateField()

    def __str__(self):
        return self.user.get_full_name()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    enrollment_date = models.DateField()

    def __str__(self):
        return self.user.get_full_name()


class Subject(models.Model):
    name = models.CharField(max_length=100)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Staff, on_delete=models.CASCADE, limit_choices_to={'role': 'T'})
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Staff, on_delete=models.CASCADE, limit_choices_to={'role': 'T'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LessonPlan(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    plan_details = models.TextField()

    def __str__(self):
        return f"Plan for {self.lesson.title}"


class LessonNote(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    note_details = models.TextField()

    def __str__(self):
        return f"Note for {self.lesson.title}"


class GmeetClass(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    meet_link = models.URLField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"GMeet: {self.lesson.title}"


class Quiz(models.Model):
    QUIZ_TYPE_CHOICES = [
        ('EXAM', 'Exam'),
        ('TEST', 'Test'),
        ('HW', 'Homework'),
    ]
    title = models.CharField(max_length=255)
    quiz_type = models.CharField(max_length=10, choices=QUIZ_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(Student)
    due_date = models.DateField()

    def __str__(self):
        return self.title


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.quiz.title}"


class SchoolSettings(models.Model):
    school = models.OneToOneField(School, on_delete=models.CASCADE)
    settings_data = models.JSONField()

    def __str__(self):
        return f"Settings for {self.school.name}"

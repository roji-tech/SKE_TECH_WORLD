from django.db import models
from django.contrib.auth.models import AbstractUser

# School Model


class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    logo = models.ImageField(upload_to='school_logos/', null=True, blank=True)

    def __str__(self):
        return self.name

# Academic Session Model


class AcademicSession(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.start_year}/{self.end_year}"

# Term Model


class Term(models.Model):
    name = models.CharField(max_length=50)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.session}"

# Classroom Model


class Classroom(models.Model):
    name = models.CharField(max_length=50)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    grade_level = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Custom User Model for Staff and Students


class User(AbstractUser):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, null=True, blank=True)
    is_staff_member = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

# Staff Model


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)  # E.g., Teacher, Accountant, etc.
    is_teaching_staff = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()

# Student Model


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        Classroom, on_delete=models.SET_NULL, null=True)
    admission_date = models.DateField()

    def __str__(self):
        return self.user.get_full_name()

# Subject Model


class Subject(models.Model):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

# Lesson Model


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.topic

# Lesson Plan Model


class LessonPlan(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    objectives = models.TextField()

# Lesson Note Model


class LessonNote(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    content = models.TextField()

# Gmeet Class Model


class GmeetClass(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    link = models.URLField()

# School Settings Model


class SchoolSettings(models.Model):
    school = models.OneToOneField(School, on_delete=models.CASCADE)
    grading_system = models.JSONField()  # E.g., {"A": "90-100", "B": "80-89"}

# Quiz Model


class Quiz(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)  # E.g., Test, Homework, Exam
    due_date = models.DateField()

# Quiz Question Model


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    options = models.JSONField()  # E.g., {"A": "Option A", "B": "Option B"}
    correct_option = models.CharField(max_length=1)

# Quiz Result Model


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField()

# Question Bank Model


class QuestionBank(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question = models.TextField()
    options = models.JSONField()
    correct_option = models.CharField(max_length=1)

# Result Model


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    total_score = models.FloatField()
    grade = models.CharField(max_length=2)

# Event Model


class Event(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()

# Notification Model


class Notification(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    message = models.TextField()
    # E.g., General, Staff, Students
    audience_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

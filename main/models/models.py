from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

from main.models.users import User


class School(TenantMixin):
    # class School(models.Model):
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='owned_school')
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    domain = models.CharField(max_length=128)
    school = models.ForeignKey(
        School, related_name='domains', on_delete=models.CASCADE)


class AcademicSession(models.Model):
    TERM_CHOICES = (
        ('1st', '1st Term'),
        ('2nd', '2nd Term'),
        ('3rd', '3rd Term'),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    term = models.CharField(max_length=4, choices=TERM_CHOICES)

    def __str__(self):
        return self.name


class AcademicSession(models.Model):
    TERM_CHOICES = [
        ('1st', '1st Term'),
        ('2nd', '2nd Term'),
        ('3rd', '3rd Term'),
    ]
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    term = models.CharField(max_length=4, choices=TERM_CHOICES)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.term}"


class SchoolClass(models.Model):
    CLASS_CHOICES = [
        ('KG1', 'Kindergarten 1'),
        ('KG2', 'Kindergarten 2'),
        ('KG3', 'Kindergarten 3'),
        ('PRY1', 'Primary 1'),
        ('PRY2', 'Primary 2'),
        ('PRY3', 'Primary 3'),
        ('PRY4', 'Primary 4'),
        ('PRY5', 'Primary 5'),
        ('PRY6', 'Primary 6'),
        ('JS1', 'Junior Secondary 1'),
        ('JS2', 'Junior Secondary 2'),
        ('JS3', 'Junior Secondary 3'),
        ('SS1', 'Senior Secondary 1'),
        ('SS2', 'Senior Secondary 2'),
        ('SS3', 'Senior Secondary 3'),
    ]

    name = models.CharField(max_length=4, choices=CLASS_CHOICES)
    academic_session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE)
    class_teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_teacher': True})

    def __str__(self):
        return f"{self.name} - {self.get_name_display()}"


class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    assigned_classes = models.ManyToManyField(
        SchoolClass, related_name='subjects')
    teacher = models.ForeignKey(
        'T', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class GmeetClass(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    gmeet_link = models.URLField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'{self.subject.name} on {self.date}'


class LessonPlan(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject.name


class ClassNote(models.Model):
    lesson_plan = models.ForeignKey(LessonPlan, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lesson_plan.subject.name


class LibraryBook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    available_copies = models.IntegerField()

    def __str__(self):
        return self.title


class Examination(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'{self.subject.name} Exam on {self.date}'


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.student.name} - {self.examination.subject.name}'


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return self.subject.name


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    obtained_marks = models.IntegerField()

    def __str__(self):
        return self.student.name


class Setting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key

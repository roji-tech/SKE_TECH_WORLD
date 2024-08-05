from django.db import models


class AcademicSession(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=100)
    academic_session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    roll_number = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class GmeetClass(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    link = models.URLField()

    def __str__(self):
        return f'{self.subject.name} on {self.date}'


class LessonPlan(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.subject.name


class ClassNote(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.subject.name


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

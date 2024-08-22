from django.db import models
from .users import User
from .models import AcademicSession, SchoolClass, Subject
from django.utils.crypto import get_random_string


from django.db import models
from django.contrib.auth.models import User
from datetime import date


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, primary_key=True, unique=True)
    date_of_birth = models.DateField()
    admission_date = models.DateField(default=date.today)
    student_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, null=True, blank=True)

    academic_year = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, null=True, blank=True)  # e.g., 2023/2024
    reg_no = models.CharField(max_length=20, unique=True)

    picture = models.ImageField(
        upload_to='student_pictures/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically generate student_id with school_id as prefix
        if not self.student_id:
            school_id = self.school_class.school.id
            self.student_id = f"{school_id}-{self.reg_no}"
        super(StudentProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.student_id})"

    def get_age(self):
        # Helper method to calculate the student's age
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (
                self.date_of_birth.month, self.date_of_birth.day)
        )


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True, primary_key=True)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.id} - {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.student_id:
            # Pad the school ID to ensure a consistent format
            school_id = str(self.school_class.school.id).zfill(4)
            unique_suffix = get_random_string(
                length=6, allowed_chars='0123456789')
            self.student_id = f"{school_id}-{unique_suffix}"
        super().save(*args, **kwargs)


class Teacher(models.Model):
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

    DEPARTMENT_CHOICES = [
    ('S', 'Science'),
    ('H', 'Humanity'),
    ('B', 'Business'),
    ('O', 'Other'),
]

    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)
    # extending the model
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    department = models.CharField(max_length=1, choices=DEPARTMENT_CHOICES)
    specifications = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='images/teachers_images/', blank=True, null=True)



    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    class_assigned = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    roll_number = models.IntegerField()

    def __str__(self):
        return self.name

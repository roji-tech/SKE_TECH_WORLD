from django.contrib.auth import get_user_model
from datetime import date

from django.utils.crypto import get_random_string
from .users import OWNER
from django.db import models
import string

User = get_user_model()


class School(models.Model):
    # class School(models.Model):
    name = models.CharField(max_length=50)
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='school')
    address = models.TextField(default="")
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    logo = models.URLField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_user_school(user: User):
        print(user, user.role, School.objects.filter(owner=user))
        if user.role == OWNER:
            return School.objects.filter(owner=user).first()
        return user.school


class AcademicSession(models.Model):

    def __str__(self):
        return f"{self.name} ({self.school.name})"

    class Meta:
        unique_together = ('school', 'name')

    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='academic_sessions')
    name = models.CharField(max_length=100)  # e.g., "2023/2024"
    start_date = models.DateField()
    end_date = models.DateField()
    next_session_begins = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    max_exam_score = models.SmallIntegerField(default=60)

    def get_year_from_date(self, date_string):
        # Split the date string by hyphen and return the first part as an integer
        try:
            year = int(date_string.split('-')[0])
            return year
        except (ValueError, IndexError):
            # Handle cases where the date string is not in the expected format
            raise ValueError(f"Invalid date format: '{
                             date_string}'. Expected format 'YYYY-MM-DD'.")

    def save(self, *args, **kwargs):
        get_year_from_date = self.get_year_from_date

        if not self.name:  # Set the name only if it's not already set
            try:
                self.name = f"{self.start_date.year}-{self.end_date.year}"
            except Exception as e:
                year1 = get_year_from_date(self.start_date)
                year2 = get_year_from_date(self.end_date)
                self.name = f"{year1}-{year2}"

        # Attempt to split and convert the name parts to integers
        try:
            name_parts = self.name.split('-')
            existing_start_year = int(name_parts[0])
            existing_end_year = int(name_parts[1]) if len(
                name_parts) > 1 else existing_start_year
       
            # If both years are the same, update the name to just the year
            if existing_start_year == existing_end_year:
                self.name = str(existing_start_year)
        except (ValueError, IndexError):
            year1 = get_year_from_date(self.start_date)
            year2 = get_year_from_date(self.end_date)
            self.name = f"{year1}-{year2}"


        self.save(*args, **kwargs)

    @staticmethod
    def get_school_sessions(request):
        user = request.user
        school = School.objects.filter(owner=user).first()
        return AcademicSession.objects.filter(school=school)


class Term(models.Model):
    TERM_CHOICES = [
        ('1st', '1st Term'),
        ('2nd', '2nd Term'),
        ('3rd', '3rd Term'),
    ]
    academic_session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, related_name='terms')
    name = models.CharField(max_length=4, choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    next_term_begins = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('academic_session', 'name')

    def __str__(self):
        return f"{self.name} ({self.academic_session.name})"


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='teacher_profile')
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='teachers')
    department = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.department} - {self.user.full_name}"

    def get_school_teachers(request):
        user = request.user
        school = School.get_user_school(user)
        return Teacher.objects.filter(school=school).select_related("user")

    @property
    def full_name(self):
        return f"{self.user.full_name}"

    @property
    def phone(self):
        return f"{self.user.phone}"


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

    CLASS_CATEGORIES = (
        ("ART", "Art Class"),
        ("SCIENCE", "Science Class"),
        ("COMMERCIAL", "Commercial Class"),
    )

    DIVISION_CHOICES = [(letter, letter) for letter in string.ascii_uppercase]

    # school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=4, choices=CLASS_CHOICES)
    academic_session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, related_name='classes')
    class_teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': "teacher"}, related_name="school_class")
    division = models.CharField(
        max_length=10,  blank=True, null=True,
        choices=DIVISION_CHOICES
    )  # e.g., "A", "B", "C"
    category = models.CharField(
        max_length=12, choices=CLASS_CATEGORIES, blank=True, null=True)

    def __str__(self):
        return f"{self.get_name_display()} ({self.academic_session.name})"

    class Meta:
        unique_together = ('academic_session', 'name', 'division')

    def __str__(self):
        try:
            return f"{self.name} {self.division.name if self.division else ''} ({self.academic_session.name})"
        except:
            return f"{self.name}({self.academic_session.name})"

    @staticmethod
    def get_school_classes(request):
        user = request.user
        school = School.objects.filter(owner=user).first()
        print(SchoolClass.objects.filter(academic_session__school=school))
        return SchoolClass.objects.filter(academic_session__school=school)


class Student(models.Model):
    reg_no = models.CharField(
        max_length=20, null=True, blank=True, unique=True)
    student_id = models.CharField(
        max_length=20, unique=True, null=True, blank=True)
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='students')
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='student_profile')
    date_of_birth = models.DateField()
    admission_date = models.DateField(default=date.today)
    student_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, related_name='students', null=True, blank=True)

    academic_year = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, null=True, blank=True)  # e.g., 2023/2024

    def get_school_students(request):
        user = request.user
        school = School.get_user_school(user)
        return Student.objects.filter(school=school).select_related("user", "student_class").order_by("student_class")

    @property
    def student_age(self):
        # Helper method to calculate the student's age
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (
                self.date_of_birth.month, self.date_of_birth.day)
        )

    def __str__(self):
        return f"{self.id} - {self.user.full_name}"

    @property
    def full_name(self):
        return f"{self.user.full_name}"

    def save(self, *args, **kwargs):
        if not self.student_id:  # Check if student_id is not set
            self.student_id = f"STU-{self.admission_date.year}-{self.id}"
            super().save(*args, **kwargs)  # Save first to get the ID
        else:
            super().save(*args, **kwargs)  # Save as usual if student_id is already set


class Subject(models.Model):
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name="subjects")

    class Meta:
        unique_together = ('school_class', 'name')

    def __str__(self):
        return f"{self.name} - {self.school_class.name}"

    @staticmethod
    def get_school_subjects(request):
        """Retrieves all subjects associated with the current user's school.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            QuerySet: A QuerySet of Subject objects.
        """

        user = request.user
        school = School.objects.filter(owner=user).first()

        if school:
            return Subject.objects.filter(school_class__academic_session__school=school)
        else:
            # Return an empty QuerySet if the user doesn't belong to a school
            return Subject.objects.none()


class GmeetClass(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='gmeet_classes')
    description = models.TextField()
    gmeet_link = models.URLField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject.name} - {self.subject.school_class.name} ({self.start_time})"


class LessonPlan(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='lesson_plans')
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_file = models.FileField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return f"{self.uploaded_file.name} uploaded by {self.uploaded_by.username}"


class ClassNote(models.Model):
    lesson_plan = models.ForeignKey(
        LessonPlan, on_delete=models.CASCADE, related_name='class_notes')
    title = models.CharField(max_length=255)
    for_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, related_name='+')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.URLField()

    def __str__(self):
        return f"Note for {self.lesson_plan.subject.name} ({self.lesson_plan.subject.school_class.name})"


class Examination(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='examinations')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='examinations')
    term = models.ForeignKey(
        Term, on_delete=models.CASCADE, related_name='examinations')
    date = models.DateField()
    # score = models.DecimalField(
    #     max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.subject.name} Exam - {self.term.name}"

    class Meta:
        unique_together = ('subject', 'term')


class ContinuousAssessment(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='continuous_assessments')
    file = models.FileField(
        upload_to='assessment/%Y/%m/%d/', null=True, blank=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='continuous_assessments')
    name = models.CharField(max_length=100)
    score = models.DecimalField(
        max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('subject', 'student', 'name')

    def __str__(self):
        return f"{self.name} - {self.subject.name} - {self.student.user.get_full_name()}"


class Score(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.student.name} - {self.examination.subject.name}'


class Result(models.Model):
    examination = models.ForeignKey(
        Examination, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='results')
    # Score from the main exam
    score = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('examination', 'student')

    def __str__(self):
        return f"Result for {self.student.user.get_full_name()} - {self.examination.subject.name}"

    def total_score_with_ca(self):
        # Calculate the total score by adding exam score and all CA scores
        ca_score = sum(ca.score for ca in self.student.continuous_assessments.filter(
            subject=self.examination.subject))
        return self.score + ca_score


class SchoolSettings(models.Model):
    school = models.OneToOneField(
        School, on_delete=models.CASCADE, related_name='settings')
    grading_system = models.TextField()  # e.g., "A: 90-100, B: 80-89, ..."
    attendance_policy = models.TextField()

    def __str__(self):
        return f"Settings for {self.school.name}"


# class SettingItem(models.Model):
#     key = models.CharField(max_length=100, unique=True)
#     value = models.CharField(max_length=200)

#     def __str__(self):
#         return self.key


class Library(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name='library')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class LibraryBook(models.Model):
    library = models.ForeignKey(
        Library, on_delete=models.CASCADE, related_name="library")
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    available_copies = models.IntegerField()

    def __str__(self):
        return self.title

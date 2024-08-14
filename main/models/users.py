from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("superadmin", "Super Admin"),
        ("owner", "School Owner"),
        ("admin", "Admin"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    )

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def is_superadmin(self):
        return self.role == "superadmin"

    def is_owner(self):
        return self.role == "owner"

    def is_admin(self):
        return self.role in ["admin", "owner"]

    def is_teacher(self):
        return self.role == "teacher"

    def is_student(self):
        return self.role == "student"

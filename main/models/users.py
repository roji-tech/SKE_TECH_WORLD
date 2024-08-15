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

    @property
    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return "{} ({})".format(self.username, self.get_full_name)

    @property
    def get_user_role(self):
        if self.role == "superadmin":
            role = "Super Admin"
        elif self.role in ["admin", "owner"]:
            role = "School Admin"
        elif self.role == "teacher":
            role = "Teacher"
        elif self.role == "student":
            role = "Student"

        return role

    def save(self, *args, **kwargs):
        try:
            # if self.is_superadmin():
            #     self.is_superadmin == True
            ...
        except:
            pass
        super().save(*args, **kwargs)

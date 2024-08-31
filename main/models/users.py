from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


SUPERADMIN = "superadmin"
OWNER = "owner"
ADMIN = "admin"
TEACHER = "teacher"
STUDENT = "student"


class User(AbstractUser):
    ROLE_CHOICES = (
        (SUPERADMIN, "Super Admin"),
        (OWNER, "School Owner"),
        (ADMIN, "Admin"),
        (TEACHER, "Teacher"),
        (STUDENT, "Student"),
    )

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["role"]

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    )

    email = models.EmailField(_("email address"), blank=True, unique=True,
                              error_messages={"unique": _(f"An Admin, Teacher or Student with that email already exists."), })
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    image = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, default="+234----")

    @property
    def is_superadmin(self):
        return self.role == "superadmin"

    @property
    def is_owner(self):
        return self.role == "owner"

    @property
    def is_admin(self):
        return self.role in ["admin", "owner"]

    @property
    def is_teacher(self):
        return self.role == "teacher"

    @property
    def is_student(self):
        return self.role == "student"

    @property
    def full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return "{} ({})".format(self.username, self.full_name)

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

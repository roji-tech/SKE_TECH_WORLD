from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

SUPERADMIN = "superadmin"
OWNER = "owner"
ADMIN = "admin"
TEACHER = "teacher"
STUDENT = "student"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


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
    REQUIRED_FIELDS = ['role']

    username = None  # Remove the username field
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=10, default=STUDENT, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    image = models.ImageField(blank=True, null=True)
    phone = models.CharField(max_length=20, default="+234----")

    objects = UserManager()

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
        full_name = self.email  # Using email if first_name and last_name are empty
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return "{} ({})".format(self.email, self.full_name)

    @property
    def get_user_role(self):
        roles = {
            "superadmin": "Super Admin",
            "admin": "School Admin",
            "owner": "School Admin",
            "teacher": "Teacher",
            "student": "Student"
        }
        return roles.get(self.role, "Unknown Role")

    def save(self, *args, **kwargs):
        try:
            # Custom save logic, if needed
            if (self.is_teacher or self.is_student) and not self.password:
                self.set_password(str(self.last_name).lower())
        except Exception as e:
            pass
        super().save(*args, **kwargs)


# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils.translation import gettext_lazy as _


# SUPERADMIN = "superadmin"
# OWNER = "owner"
# ADMIN = "admin"
# TEACHER = "teacher"
# STUDENT = "student"


# class User(AbstractUser):
#     ROLE_CHOICES = (
#         (SUPERADMIN, "Super Admin"),
#         (OWNER, "School Owner"),
#         (ADMIN, "Admin"),
#         (TEACHER, "Teacher"),
#         (STUDENT, "Student"),
#     )

#     GENDER_CHOICES = (
#         ("M", "Male"),
#         ("F", "Female"),
#     )

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ["role"]

#     username = models.CharField(
#         _("username"),
#         max_length=50,
#         help_text=_(
#             "Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."
#         ),
#         null=True,
#         blank=True
#     )

#     email = models.EmailField(_("email address"), blank=True, unique=True,
#                               error_messages={"unique": _(f"An Admin, Teacher or Student with that email already exists."), })
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
#     image = models.URLField(blank=True, null=True)
#     phone = models.CharField(max_length=20, default="+234----")

#     @property
#     def is_superadmin(self):
#         return self.role == "superadmin"

#     @property
#     def is_owner(self):
#         return self.role == "owner"

#     @property
#     def is_admin(self):
#         return self.role in ["admin", "owner"]

#     @property
#     def is_teacher(self):
#         return self.role == "teacher"

#     @property
#     def is_student(self):
#         return self.role == "student"

#     @property
#     def full_name(self):
#         full_name = self.username
#         if self.first_name and self.last_name:
#             full_name = self.first_name + " " + self.last_name
#         return full_name

#     def __str__(self):
#         return "{} ({})".format(self.username, self.full_name)

#     @property
#     def get_user_role(self):
#         if self.role == "superadmin":
#             role = "Super Admin"
#         elif self.role in ["admin", "owner"]:
#             role = "School Admin"
#         elif self.role == "teacher":
#             role = "Teacher"
#         elif self.role == "student":
#             role = "Student"

#         return role

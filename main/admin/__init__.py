from django.contrib import admin
from ..models import (
    User, School, AcademicSession,
    LessonPlan, ClassNote, SchoolClass,
    Student, Subject, Teacher,
    GmeetClass
)


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "role",
        "id",
        "get_full_name",
        "email",
        "gender",
        "is_active",
        # "is_teacher",
        "is_student",
        "is_admin",
        "is_teacher",
    ]
    search_fields = [
        # "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        # "is_teacher",
        "is_student",
        "is_admin",
    ]

    class Meta:
        managed = True
        verbose_name = "User"
        verbose_name_plural = "Users"


class SchoolAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "id",
    ]


class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = [
        "name", "school",
        "is_current", "id",
    ]


class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        "full_name", "phone", "department",
        "id", "school",
    ]


class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "full_name", "email",
        "id", "school", 'klass',
        "student_class",
    ]


class ClassAdmin(admin.ModelAdmin):
    list_display = [
        "name", "division",
        "category", "academic_session",
    ]


admin.site.register(User, UserAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(AcademicSession, AcademicSessionAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject)
admin.site.register(SchoolClass, ClassAdmin)
admin.site.register(ClassNote)
admin.site.register(LessonPlan)
admin.site.register(GmeetClass)

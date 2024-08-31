from django.contrib import admin
from ..models import User, School, AcademicSession, LessonPlan, ClassNote, SchoolClass, Student, Subject, Teacher


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "get_full_name",
        # "username",
        "email",
        "role",
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


class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        "full_name", "phone",
        "id", "school",
    ]


admin.site.register(User, UserAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(AcademicSession)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(SchoolClass)
admin.site.register(ClassNote)
admin.site.register(LessonPlan)
# admin.site.register(Student)
# admin.site.register(Parent)

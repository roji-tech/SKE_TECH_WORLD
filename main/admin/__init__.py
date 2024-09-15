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
        "id", "school", "email",
    ]


class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "full_name", "email", 'reg_no',
        "id", "school", 'klass',
        "student_class",
    ]


class ClassAdmin(admin.ModelAdmin):
    list_display = [
        "name", "division",
        "category", "academic_session",
    ]


class GmeetClassAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'title', 'created_by',
                    'subject', 'gmeet_link', 'duration']
    list_filter = ['subject', 'start_time', 'created_by']
    search_fields = ['subject__name', 'description', 'gmeet_link']
    # date_hierarchy = 'start_time'
    ordering = ['start_time']
    fields = ['created_by', 'title', 'subject', 'description',
              'gmeet_link', 'start_time', 'duration', ]

    # Make sure the created_by field is automatically populated with the current user in the admin panel
    # def save_model(self, request, obj, form, change):
    #     if not obj.created_by:
    #         obj.created_by = request.user
    #     super().save_model(request, obj, form, change)


# Register the GmeetClass model with the customized admin interface
admin.site.register(GmeetClass, GmeetClassAdmin)

admin.site.register(User, UserAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(AcademicSession, AcademicSessionAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject)
admin.site.register(SchoolClass, ClassAdmin)
admin.site.register(ClassNote)
admin.site.register(LessonPlan)

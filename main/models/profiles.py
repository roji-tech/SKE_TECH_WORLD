# from django.core.exceptions import ObjectDoesNotExist
# import logging
# from django.urls import path
# from django.http import HttpResponse
# from django.utils.encoding import force_str
# from django.utils.http import urlsafe_base64_decode
# from django.utils.crypto import get_random_string
# from django.core.mail import send_mail
# from django.conf import settings
# from django.urls import reverse
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.template.loader import render_to_string
# from django.contrib.sites.shortcuts import get_current_site
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from datetime import date


# class Student(models.Model):
#     reg_no = models.CharField(
#         max_length=20, null=True, blank=True, unique=True)
#     # Increased length for new format
#     student_id = models.CharField(
#         max_length=12, unique=True, null=True, blank=True)
#     school = models.ForeignKey(
#         School, on_delete=models.CASCADE, related_name='students')
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, related_name='student_profile')
#     date_of_birth = models.DateField()
#     student_class = models.ForeignKey(
#         SchoolClass, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
#     session_admitted = models.ForeignKey(
#         AcademicSession, on_delete=models.CASCADE, null=True, blank=True)  # e.g., 2023/2024

#     def save(self, *args, **kwargs):
#         # Generate a unique student ID if it's not already set
#         if not self.student_id:
#             self.student_id = self.generate_unique_student_id()

#         # Generate a unique dynamic email if not set
#         if not self.user.email:
#             self.user.email = self.generate_unique_email()
#             self.user.save()

#         super().save(*args, **kwargs)

#     def generate_unique_student_id(self):
#         """Generates a unique student ID based on the school and admission year."""
#         # Extract short school name (e.g., first 3 letters)
#         school_short_name = self.school.short_name[:3].upper(
#         ) if self.school.short_name else "SCH"
#         # Admission year (last 2 digits of current year)
#         admission_year = str(self.session_admitted.start_date.year)[-2:]

#         # Find the last student in the same school and admission year
#         last_student = Student.objects.filter(
#             school=self.school, session_admitted=self.session_admitted
#         ).order_by('student_id').last()

#         if last_student and last_student.student_id:
#             # Extract the last 3 digits and increment
#             last_number = int(last_student.student_id.split('-')[-1])
#             new_number = str(last_number + 1).zfill(3)
#         else:
#             new_number = "001"  # Start from 001 if no previous student

#         return f"{school_short_name}{admission_year}-{new_number}"

#     def generate_unique_email(self):
#         """Generates a unique dynamic email for the student."""
#         school_short_name = self.school.short_name.lower(
#         ) if self.school.short_name else "school"
#         admission_year = str(self.session_admitted.start_date.year)[-2:]
#         base_email = f"{self.user.first_name.lower()}.{
#             self.user.last_name.lower()}@{school_short_name}{admission_year}.com"
#         unique_email = base_email

#         # Ensure the email is unique
#         counter = 1
#         while User.objects.filter(email=unique_email).exists():
#             unique_email = f"{self.user.first_name.lower()}.{self.user.last_name.lower()}{
#                 counter}@{school_short_name}{admission_year}.com"
#             counter += 1

#         return unique_email

#     def __str__(self):
#         return f"{self.student_id} - {self.user.full_name}"

# # Signal to trigger email verification after student creation


# @receiver(post_save, sender=Student)
# def send_verification_email(sender, instance, created, **kwargs):
#     if created:
#         user = instance.user
#         send_verification_email_to_user(user)


# def send_verification_email_to_user(user):
#     token = default_token_generator.make_token(user)
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     current_site = get_current_site(None)  # Assuming a request is available
#     mail_subject = 'Activate your account'
#     message = render_to_string('account/activate_email.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': uid,
#         'token': token,
#     })
#     send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])

# # In your urls.py


# urlpatterns = [
#     path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
# ]

# # In your views.py


# def activate_account(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return HttpResponse('Thank you for your email confirmation. Your account is now active.')
#     else:
#         return HttpResponse('Activation link is invalid!')


# class Student(models.Model):
#     reg_no = models.CharField(
#         max_length=20, null=True, blank=True, unique=True)
#     student_id = models.CharField(
#         max_length=6, unique=True, null=True, blank=True)
#     school = models.ForeignKey(
#         School, on_delete=models.CASCADE, related_name='students')
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, related_name='student_profile')
#     date_of_birth = models.DateField()
#     student_class = models.ForeignKey(
#         SchoolClass, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
#     session_admitted = models.ForeignKey(
#         AcademicSession, on_delete=models.CASCADE, null=True, blank=True)  # e.g., 2023/2024

#     def save(self, *args, **kwargs):
#         # Generate a unique student ID if it's not already set
#         if not self.student_id:
#             self.student_id = self.generate_unique_student_id()

#         # Generate a unique dynamic email if not set
#         if not self.user.email:
#             self.user.email = self.generate_unique_email()
#             self.user.save()

#         super().save(*args, **kwargs)

#     def generate_unique_student_id(self):
#         """Generates a unique 6-character student ID for the student."""
#         unique_id = get_random_string(
#             6, allowed_chars='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#         while Student.objects.filter(student_id=unique_id).exists():
#             unique_id = get_random_string(
#                 6, allowed_chars='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#         return unique_id

#     def generate_unique_email(self):
#         """Generates a unique dynamic email for the student."""
#         school_short_name = self.school.short_name.lower(
#         ) if self.school.short_name else "school"
#         base_email = f"{self.user.first_name.lower()}.{
#             self.user.last_name.lower()}@{school_short_name}.com"
#         unique_email = base_email

#         # Ensure the email is unique
#         counter = 1
#         while User.objects.filter(email=unique_email).exists():
#             unique_email = f"{self.user.first_name.lower()}.{self.user.last_name.lower()}{
#                 counter}@{school_short_name}.com"
#             counter += 1

#         return unique_email

#     def __str__(self):
#         return f"{self.student_id} - {self.user.full_name}"

# # Signal to trigger email verification after student creation



# # In your urls.py



# # In your views.py



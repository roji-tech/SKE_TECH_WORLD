from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model



from .models import Notification
from main.models.models import Teacher

User = get_user_model()


# @receiver(post_save, sender=Teacher)
# def notify_teacher_added(sender, instance, added, **kwargs):
#   if added:
#     message = f"New teacher '{instance.full_name}' has been added"
#   else:
#     message = f"New teacher '{instance.full_name}' has been updated"

#   send_notification(instance, message)
@receiver(post_save, sender=Teacher)
def notify_teacher_creation(sender, instance, created, **kwargs):
    if created:
        # Create a notification when a new teacher is added
        Notification.objects.create(
            title="New teacher added",
            message=f"Teacher {instance.full_name} has been added to the system.",
            user=instance.created_by
        )

def send_notification(instance, message):

  recipients = User.objects.filter(is_admin=True)

  for recipient in recipients:
    Notification.objects.create(instance=instance, message=message, recipient=recipient)
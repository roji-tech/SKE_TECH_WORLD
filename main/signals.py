from django.dispatch import Signal, receiver
from django.db.models.signals import post_save

from main.models.models import Teacher
from notification.models import Notification

# New user has registered. Args: user, request.
user_registered = Signal()

# User has activated his or her account. Args: user, request.
user_activated = Signal()

# User has been updated. Args: user, request.
user_updated = Signal()

@receiver(post_save, sender=Teacher)
def notify_teacher_creation(sender, instance, created, **kwargs):
    if created:
        # Create a notification when a new teacher is added
        Notification.objects.create(
            title="New teacher added",
            message=f"Teacher {instance.full_name} has been added to the system.",
            user=instance.user
        )

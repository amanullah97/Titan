from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Patient, Notification


@receiver(post_save, sender=Patient)
def create_notification(sender, instance, **kwargs):
    if kwargs.get('created', False):
        message = f"New appointment created: {instance.patient.name}"
        Notification.objects.create(user=instance.patient.assistant, message=message)

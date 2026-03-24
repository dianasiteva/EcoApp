from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Participant


@receiver(post_save, sender=User)
def create_participant_profile(sender, instance, created, **kwargs):
    if created:
        Participant.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_participant_profile(sender, instance, **kwargs):
    instance.participant.save()

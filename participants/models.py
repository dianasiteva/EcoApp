from PIL import Image
from django.contrib.auth.models import User
from django.db import models

from cities.models import Cities
from events.models import Event, Role
from participants.validators import plate_validator, validate_image


class Participant(models.Model):
    contact_email = models.EmailField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, blank=True, null=True)
    car_registration_number = models.CharField(max_length=8, validators=[plate_validator], blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="participants/",
        validators=[validate_image],
        blank=True,
        null=True
    )
    appended_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_picture:
            img = Image.open(self.profile_picture.path)

            max_size = (800, 800)
            img.thumbnail(max_size, Image.LANCZOS)
            img.save(self.profile_picture.path)


    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name


class ParticipantEventRole(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    information = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['participant', 'event', 'role'],
                name='unique_participant_event_role'
            )
        ]

    def __str__(self):
        return f"{self.participant.first_name} {self.participant.last_name} → {self.event.title} ({self.role.name})"



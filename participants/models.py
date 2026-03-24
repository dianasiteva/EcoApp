from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField

from events.models import Event, Role
from participants.choises import DistrictChoice
from participants.validators import plate_validator


class Cities(models.Model):
    name = models.CharField(max_length=20)
    district = models.CharField(max_length=20, choices=DistrictChoice.choices)

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, blank=True, null=True)
    car_registration_number = models.CharField( max_length=8, validators=[plate_validator], blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True,null=True)
    appended_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name or self.user.username


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
        return f"{self.participant.user.first_name} {self.participant.user.last_name} → {self.event.title} ({self.role.name})"



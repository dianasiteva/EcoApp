from django.db import models
from events.models import Event, Role


class Participant(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    appended_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class ParticipantEventRole(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    information = models.TextField(blank=True)

    class Meta:
        unique_together = ('participant', 'event', 'role')

    def __str__(self):
        return f"{self.participant.first_name} {self.participant.last_name} → {self.event.title} ({self.role.name})"

from django.db import models

from accounts.models import AppUser
from participants.choises import DistrictChoice


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    district = models.CharField(max_length=20, choices=DistrictChoice.choices,blank=True,null=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='locations')

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name



class Event(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    report = models.TextField(blank=True,null=True)

    class Meta:
        verbose_name = "Събитие"
        verbose_name_plural = "Събития"
        permissions = [
            ("edit_report", "Може да редактира отчет"),
        ]

    def __str__(self):
        return f"{self.title} – {self.date}"



class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=150,blank=True)

    class Meta:
        verbose_name = "Роля"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.name


from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name



class Event(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} – {self.date}"


class Role(models.Model):
    name = models.CharField(max_length=20)  # Organizer, Volunteer, Sponsor, Logistician, etc.
    description = models.TextField(max_length=150,blank=True)

    def __str__(self):
        return self.name

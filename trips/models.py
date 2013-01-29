from django.db import models
from django.contrib.auth.models import User


class Trip(models.Model):
    TRAVELLING_BY_CHOICES = (
        (1, 'Plane'),
        (2, 'Bus'),
        (3, 'Car'),
        (4, 'Train'),
    )
    user = models.ForeignKey(User)
    departure_city = models.CharField(max_length=255)
    departure_dt = models.DateTimeField()
    destination_city = models.CharField(max_length=255)
    destination_dt = models.DateTimeField()
    travelling_by = models.IntegerField(choices=TRAVELLING_BY_CHOICES)
    comments = models.TextField(blank=True)
    creation_dt = models.DateTimeField(auto_now_add=True)

    @property
    def get_departure_city(self):
        return self.departure_city.split(',')[0].strip()

    @property
    def get_departure_country(self):
        return self.departure_city.split(',')[-1].strip()

    @property
    def get_destination_city(self):
        return self.destination_city.split(',')[0].strip()

    @property
    def get_destination_country(self):
        return self.destination_city.split(',')[-1].strip()


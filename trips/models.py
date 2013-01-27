from django.db import models


class Trip(models.Model):
    departure_city = models.CharField(max_length=255)
    departure_dt = models.DateTimeField()
    destination_city = models.CharField(max_length=255)
    destination_dt = models.DateTimeField()


from django.db import models
from django.contrib.auth.models import User


class Trip(models.Model):
    user = models.ForeignKey(User)
    departure_city = models.CharField(max_length=255)
    departure_dt = models.DateTimeField()
    destination_city = models.CharField(max_length=255)
    destination_dt = models.DateTimeField()


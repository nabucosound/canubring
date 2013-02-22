from django.db import models
from django.contrib.auth.models import User

from trips.models import Trip


class Cargo(models.Model):
    CARGO_STATE_CHOICES = (
        (0, 'Open'),
        (1, 'Handshake'),
        (2, 'Closed'),
    )
    trip = models.ForeignKey(Trip)
    requesting_user = models.ForeignKey(User, related_name='my_cargos')
    traveller_user = models.ForeignKey(User, related_name='requested_cargos')
    state = models.IntegerField(choices=CARGO_STATE_CHOICES, default=0)

    def __unicode__(self):
        return u"Cargo from %s to %s" % (self.trip.departure_city, self.trip.destination_city)


class CargoComment(models.Model):
    cargo = models.ForeignKey(Cargo)
    user = models.ForeignKey(User)
    content = models.TextField()


from django.db import models
from django.contrib.auth.models import User
from cities_light.models import Country, City


class Trip(models.Model):
    TRAVELLING_BY_CHOICES = (
        (1, 'Plane'),
        (2, 'Bus'),
        (3, 'Car'),
        (4, 'Train'),
    )
    user = models.ForeignKey(User)
    travelling_by = models.IntegerField(choices=TRAVELLING_BY_CHOICES)
    comments = models.TextField(blank=True)
    creation_dt = models.DateTimeField(auto_now_add=True)
    dep_city = models.ForeignKey(City, related_name='dep_city_trips')
    dep_country = models.ForeignKey(Country, related_name='dep_country_trips')
    dest_city = models.ForeignKey(City, related_name='dest_city_trips')
    dest_country = models.ForeignKey(Country, related_name='dest_country_trips')
    destination_dt = models.DateTimeField()
    # Legacy
    uid = models.CharField(max_length=36, blank=True)

    def __unicode__(self):
        return u"From %s to %s" % (self.dep_city, self.dest_city)

    def save(self, *args, **kwargs):
        super(Trip, self).save(*args, **kwargs)

    @property
    def get_departure_city(self):
        return self.dep_city.name

    @property
    def get_departure_country(self):
        return self.dep_country.name

    @property
    def get_destination_city(self):
        return self.dest_city.name

    @property
    def get_destination_country(self):
        return self.dest_country.name

    @property
    def total_comments_count(self):
        from cargos.models import CargoComment
        return CargoComment.objects.filter(cargo__trip=self, unread=True).count()

    @property
    def total_unread_comments_count_for_owner(self):
        count = 0
        for cargo in self.cargo_set.all():
            count = count + cargo.cargocomment_set.exclude(user=self.user).filter(unread=True).count()
        return count

    @property
    def get_reviews_about_me(self):
        return self.cargo_set.exclude(traveller_user_review_stars__isnull=True)


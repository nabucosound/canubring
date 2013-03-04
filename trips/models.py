from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=255)


class Country(models.Model):
    name = models.CharField(max_length=255)


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
    dep_city = models.ForeignKey(City, blank=True, null=True, related_name='dep_city_trips')
    dep_country = models.ForeignKey(Country, blank=True, null=True, related_name='dep_country_trips')
    dest_city = models.ForeignKey(City, blank=True, null=True, related_name='dest_city_trips')
    dest_country = models.ForeignKey(Country, blank=True, null=True, related_name='dest_country_trips')

    def __unicode__(self):
        return u"From %s to %s" % (self.departure_city, self.destination_city)

    def save(self, *args, **kwargs):
        self.dep_city, created = City.objects.get_or_create(name=self.get_departure_city)
        self.dep_country, created = Country.objects.get_or_create(name=self.get_departure_country)
        self.dest_city, created = City.objects.get_or_create(name=self.get_destination_city)
        self.dest_country, created = Country.objects.get_or_create(name=self.get_destination_country)
        super(Trip, self).save(*args, **kwargs)

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

    @property
    def total_comments_count(self):
        count = 0
        for cargo in self.cargo_set.all():
            count = count + cargo.cargocomment_set.count()
        return count

    @property
    def total_unread_comments_count_for_owner(self):
        count = 0
        for cargo in self.cargo_set.all():
            count = count + cargo.cargocomment_set.exclude(user=self.user).filter(unread=True).count()
        return count

    @property
    def get_reviews_about_me(self):
        return self.cargo_set.exclude(traveller_user_review_stars__isnull=True)


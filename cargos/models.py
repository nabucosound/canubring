from django.db import models
from django.contrib.auth.models import User

from trips.models import Trip


class Cargo(models.Model):
    CARGO_STATE_CHOICES = (
        (0, 'Open'),
        (1, 'Negotiation'),
        (2, 'Handshake'),
        (3, 'Delivered'),
    )
    PICKUP_CHOICES = (
        (0, 'Common place'),
        (1, 'I will buy it'),
        (2, 'His/her address'),
        (3, 'My address'),
    )
    DELIVERY_CHOICES = (
        (0, 'Common place'),
        (1, 'His/her address'),
        (2, 'My address'),
    )
    REVIEW_STAR_CHOICES = (
        (0, 'Disaster'),
        (1, 'Bad'),
        (2, 'Regular'),
        (3, 'Good'),
        (4, 'Very good'),
        (5, 'Excellent'),
    )
    trip = models.ForeignKey(Trip)
    requesting_user = models.ForeignKey(User, related_name='my_cargos')
    traveller_user = models.ForeignKey(User, related_name='requested_cargos')
    state = models.IntegerField(choices=CARGO_STATE_CHOICES, default=0)
    # Categories
    food = models.BooleanField(default=False)
    medicaments = models.BooleanField(default=False)
    duty_free = models.BooleanField(default=False)
    electronics = models.BooleanField(default=False)
    baggage = models.BooleanField(default=False)
    books = models.BooleanField(default=False)
    documents = models.BooleanField(default=False)
    personal_belongings = models.BooleanField(default=False)
    clothes = models.BooleanField(default=False)
    others = models.CharField(max_length=255, blank=True)
    # Price deal
    price = models.CharField(max_length=255, blank=True)
    # Places
    pickup = models.IntegerField(choices=PICKUP_CHOICES, blank=True, null=True)
    delivery = models.IntegerField(choices=DELIVERY_CHOICES, blank=True, null=True)
    # Review of requesting user
    requesting_user_review_stars = models.IntegerField(choices=REVIEW_STAR_CHOICES, blank=True, null=True)
    requesting_user_review_comment = models.TextField(blank=True)
    # Review of traveller user
    traveller_user_review_stars = models.IntegerField(choices=REVIEW_STAR_CHOICES, blank=True, null=True)
    traveller_user_review_comment = models.TextField(blank=True)

    def __unicode__(self):
        return u"Cargo from %s to %s" % (self.trip.departure_city, self.trip.destination_city)

    def has_unread_comments_for_traveller_user(self):
        return True if self.cargocomment_set.exclude(user=self.traveller_user).filter(unread=True) else False

    # def used_categories(self):
    #     categories = ('food', 'medicaments', 'duty_free', 'electronics', 'baggage', 'books', 'documents', 'personal_belongings', 'clothes')
    #     return filter(lambda x: getattr(self, x), categories)


class CargoComment(models.Model):
    TYPE_CHOICES = (
        (0, 'Regular comment'),
        (1, 'Cargo form sent'),
        (2, 'Cargo form confirmed'),
    )
    cargo = models.ForeignKey(Cargo)
    user = models.ForeignKey(User)
    content = models.TextField()
    unread = models.BooleanField(default=True)
    comment_type = models.IntegerField(choices=TYPE_CHOICES, default=0)
    creation_dt = models.DateTimeField(auto_now_add=True)


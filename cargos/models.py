import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from trips.models import Trip


class Cargo(models.Model):
    CARGO_STATE_CHOICES = (
        (0, 'Open'),
        (1, 'Negotiation'),
        (2, 'Handshake'),
        (3, 'Rejected'),
        (4, 'Delivered'),
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
    traveller_user = models.ForeignKey(User, related_name='cargos_for_me')
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
    # Legacy
    uid = models.CharField(max_length=36, blank=True)

    def __unicode__(self):
        return u"Cargo from %s to %s" % (self.trip.departure_city, self.trip.destination_city)

    def has_unread_comments_for_traveller_user(self):
        return True if self.cargocomment_set.exclude(user=self.traveller_user).filter(unread=True) else False

    @property
    def expired(self):
        return self.trip.destination_dt < datetime.datetime.now()

    @classmethod
    def css_class_name(self, value):
        classes = ('', 'one', 'two', 'three', 'four', 'five')
        value = int(round(value))
        try:
            return classes[value]
        except:
            return ''

    @property
    def traveller_review_css_class_name(self):
        return self.css_class_name(self.traveller_user_review_stars)

    @property
    def requesting_user_review_css_class_name(self):
        return self.css_class_name(self.requesting_user_review_stars)

    @property
    def get_comments(self):
        return self.cargocomment_set.order_by('creation_dt')

    @property
    def total_comments_count(self):
        return self.cargocomment_set.count()

    @property
    def total_unread_comments_count_for_requesting_user(self):
        return self.cargocomment_set.exclude(user=self.requesting_user).filter(unread=True)

    @property
    def total_unread_comments_count_for_traveller_user(self):
        return self.cargocomment_set.exclude(user=self.traveller_user).filter(unread=True)


class CargoComment(models.Model):
    TYPE_CHOICES = (
        (0, 'Regular comment'),
        (1, 'Cargo form sent'),
        (2, 'Cargo form confirmed'),
        (3, 'Cargo form rejected'),
    )
    cargo = models.ForeignKey(Cargo)
    user = models.ForeignKey(User)
    content = models.TextField()
    unread = models.BooleanField(default=True)
    comment_type = models.IntegerField(choices=TYPE_CHOICES, default=0)
    creation_dt = models.DateTimeField(auto_now_add=True)
    # Legacy
    uid = models.CharField(max_length=36, blank=True)

    def __unicode__(self):
        return u"%s - %s: %s..." % (self.cargo, self.user, self.content[:30])

def notify_new_cargo_comment_to_recipient(sender, instance, created, **kwargs):
    if created and instance.comment_type == 0:
        if instance.user == instance.cargo.requesting_user:
            noti_user = instance.cargo.traveller_user
        else:
            noti_user = instance.cargo.requesting_user
        instance.cargocommentnotification_set.create(user=noti_user)

post_save.connect(notify_new_cargo_comment_to_recipient, sender=CargoComment)


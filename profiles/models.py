import datetime
from urllib2 import urlopen, HTTPError

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile


from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.google import GoogleOAuth2Backend
from social_auth.backends.contrib.linkedin import LinkedinBackend

from photos.utils import get_img_url
from cargos.models import Cargo, CargoComment


class SocialLink(models.Model):
    profile = models.ForeignKey('UserProfile')
    url = models.URLField(blank=True)
    pos = models.IntegerField(default=0)

    def __unicode__(self):
        return self.url

    def get_domain_name(self):
        from urlparse import urlparse
        parse_result = urlparse(self.url)
        split_domain = parse_result.netloc.split('.')
        if len(split_domain) == 3:
            return split_domain[1].lower()
        if len(split_domain) == 1:
            return 'website'
        else:
            return split_domain[0].lower()


class ProfileCountry(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'Profile Countries'

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    PROFILE_LANG_CHOICES = (
        (1, 'en'),
        (2, 'es'),
        (3, 'pt'),
        (4, 'fr'),
    )
    user = models.OneToOneField(User)
    profile_photo = models.ImageField(upload_to='profiles')
    country = models.ForeignKey(ProfileCountry, blank=True, null=True)
    language = models.IntegerField(choices=PROFILE_LANG_CHOICES, blank=True, null=True)
    second_language = models.IntegerField(choices=PROFILE_LANG_CHOICES, blank=True, null=True)
    completed = models.BooleanField(default=False)
    # Legacy
    uid = models.CharField(max_length=36, blank=True)
    # Imagekit specs
    square = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(135, 135)], image_field='profile_photo', format='JPEG', options={'quality': 90})
    ticket = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(30, 30)], image_field='profile_photo', format='JPEG', options={'quality': 90})
    thumb = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(45, 45)], image_field='profile_photo', format='JPEG', options={'quality': 90})
    review = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(70, 70)], image_field='profile_photo', format='JPEG', options={'quality': 90})
    default_img_url = '%simg/default_profile_%s.png'

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        for pos in range(1, 8):
            obj, created = SocialLink.objects.get_or_create(profile=self, pos=pos)

    @models.permalink
    def get_absolute_url(self):
        return ('other_profile', (), {'user_id': self.user.id})

    def get_languages(self):
        if self.second_language:
            return " - ".join((self.get_language_display(), self.get_second_language_display()))
        else:
            return self.get_language_display()

    @property
    def get_square_img_url(self):
        return get_img_url(self, 'square')

    @property
    def get_ticket_img_url(self):
        return get_img_url(self, 'ticket')

    @property
    def get_thumb_img_url(self):
        return get_img_url(self, 'thumb')

    @property
    def get_review_img_url(self):
        return get_img_url(self, 'review')

    @property
    def current_trips(self):
        return self.user.trip_set.filter(departure_dt__gt=datetime.datetime.now())

    @property
    def past_trips(self):
        return self.user.trip_set.filter(departure_dt__lte=datetime.datetime.now())

    @property
    def current_cargos(self):
        return self.user.my_cargos.filter(trip__departure_dt__gt=datetime.datetime.now())

    @property
    def past_cargos(self):
        return self.user.my_cargos.filter(trip__departure_dt__lte=datetime.datetime.now())

    @property
    def get_reviews_about_me(self):
        return Cargo.objects.filter(trip__user=self.user).exclude(traveller_user_review_stars__isnull=True)

    @property
    def get_reviews_by_me(self):
        # TODO
        return []

    @property
    def get_average_reviews_about_me_score(self):
        from django.db.models import Avg
        return self.get_reviews_about_me.aggregate(Avg('traveller_user_review_stars'))

    @property
    def average_traveller_review_css_class_name(self):
        return Cargo.css_class_name(self.get_average_reviews_about_me_score['traveller_user_review_stars__avg'])

    @property
    def get_unread_trip_comments(self):
        return CargoComment.objects.filter(cargo__traveller_user=self.user, unread=True).count()

    @property
    def get_unread_cargo_comments(self):
        return CargoComment.objects.filter(cargo__requesting_user=self.user, unread=True).count()

def new_users_handler(sender, user, response, details, **kwargs):
    """If backend has returned imag url, fetch and store it in custom profile model"""
    user.is_new = True
    if user.is_new:
        if "id" in response:

            try:
                url = None
                if sender == FacebookBackend:
                    url = "http://graph.facebook.com/%s/picture?type=large" % response["id"]
                elif sender == GoogleOAuth2Backend and "picture" in response:
                    url = response["picture"]
                elif sender == LinkedinBackend and "picture-url" in response:
                    url = response["picture-url"]

                if url:
                    avatar = urlopen(url)
                    profile = UserProfile(user=user)
                    profile.profile_photo.save(slugify(user.username + " social") + '.jpg', ContentFile(avatar.read()))
                    profile.save()

            except HTTPError:
                pass

    return False

from social_auth.signals import socialauth_registered
socialauth_registered.connect(new_users_handler, sender=None)


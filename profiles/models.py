import datetime
from urllib2 import urlopen, HTTPError

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models import Avg
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.db.models.signals import post_save


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


class USState(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'US States'

    def __unicode__(self):
        return self.name


# class ProfileCountry(models.Model):
#     code = models.CharField(max_length=2)
#     name = models.CharField(max_length=64)

#     class Meta:
#         verbose_name_plural = 'Profile Countries'

#     def __unicode__(self):
#         return self.name


class UserProfile(models.Model):
    PROFILE_LANG_CHOICES = (
        (1, 'en'),
        (2, 'es'),
        (3, 'pt'),
        (4, 'fr'),
    )
    user = models.OneToOneField(User)
    profile_photo = models.ImageField(upload_to='profiles', blank=True)
    # country = models.ForeignKey(ProfileCountry, blank=True, null=True)
    language = models.IntegerField(choices=PROFILE_LANG_CHOICES, blank=True, null=True)
    second_language = models.IntegerField(choices=PROFILE_LANG_CHOICES, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
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
        if not self.uid:
            for pos in range(1, 8):
                obj, created = SocialLink.objects.get_or_create(profile=self, pos=pos)

    @models.permalink
    def get_absolute_url(self):
        return ('other_profile', (), {'user_id': self.user.id})

    def get_languages(self, sep):
        if self.second_language:
            return sep.join((self.get_language_display(), self.get_second_language_display()))
        else:
            return self.get_language_display()

    @property
    def languages_profile(self):
        return self.get_languages(' - ')

    @property
    def languages_ticket(self):
        return self.get_languages(' / ')

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
        return self.user.trip_set.filter(destination_dt__gt=datetime.datetime.now())

    @property
    def past_trips(self):
        return self.user.trip_set.filter(destination_dt__lte=datetime.datetime.now())

    @property
    def current_cargos(self):
        return self.user.my_cargos.filter(trip__destination_dt__gt=datetime.datetime.now())

    @property
    def past_cargos(self):
        return self.user.my_cargos.filter(trip__destination_dt__lte=datetime.datetime.now())

    @property
    def get_reviews_about_me(self):
        return Cargo.objects.filter(Q(requesting_user=self.user, requesting_user_review_stars__isnull=False) | Q(traveller_user=self.user, traveller_user_review_stars__isnull=False))

    @property
    def get_reviews_by_me(self):
        return Cargo.objects.filter(Q(traveller_user=self.user, requesting_user_review_stars__isnull=False) | Q(requesting_user=self.user, traveller_user_review_stars__isnull=False))

    @property
    def get_all_reviews_by_me(self):
        return Cargo.objects.filter(Q(traveller_user=self.user) | Q(requesting_user=self.user), state=4)

    @property
    def get_completed_cargos_count(self):
        return Cargo.objects.filter(traveller_user=self.user, state=4).count()

    @property
    def get_average_reviews_about_me_score(self):
        return self.get_reviews_about_me.aggregate(Avg('traveller_user_review_stars'))

    @property
    def average_traveller_review_css_class_name(self):
        return Cargo.css_class_name(self.get_average_reviews_about_me_score['traveller_user_review_stars__avg'])

    def get_unread_comments(self, filter_name):
        filters = {
            filter_name: self.user,
            'unread': True,
        }
        return CargoComment.objects.exclude(user=self.user).filter(**filters).distinct()

    @property
    def unread_trip_comments(self):
        return self.get_unread_comments('cargo__traveller_user').count()

    @property
    def get_unread_current_trip_comments(self):
        return self.get_unread_comments('cargo__traveller_user').filter(cargo__trip__destination_dt__gt=datetime.datetime.now).count()

    @property
    def get_unread_past_trip_comments(self):
        return self.get_unread_comments('cargo__traveller_user').filter(cargo__trip__destination_dt__lte=datetime.datetime.now).count()

    @property
    def unread_cargo_comments(self):
        return self.get_unread_comments('cargo__requesting_user').count()

    @property
    def get_unread_current_cargo_comments(self):
        return self.get_unread_comments('cargo__requesting_user').filter(cargo__trip__destination_dt__gt=datetime.datetime.now).count()

    @property
    def get_unread_past_cargo_comments(self):
        return self.get_unread_comments('cargo__requesting_user').filter(cargo__trip__destination_dt__lte=datetime.datetime.now).count()

    @property
    def unreviewed_by_me(self):
        from django.db.models import Q
        return Cargo.objects.filter(state=4).filter(Q(traveller_user=self.user, requesting_user_review_stars__isnull=True) | Q(requesting_user=self.user, traveller_user_review_stars__isnull=True)).distinct().count()

    @property
    def get_social_link1(self):
        return self.sociallink_set.get(pos=1)

    @property
    def get_social_link2(self):
        return self.sociallink_set.get(pos=2)

    @property
    def get_social_link3(self):
        return self.sociallink_set.get(pos=3)

    @property
    def get_social_link4(self):
        return self.sociallink_set.get(pos=4)

    @property
    def get_social_link5(self):
        return self.sociallink_set.get(pos=5)

    @property
    def get_social_link6(self):
        return self.sociallink_set.get(pos=6)

    @property
    def get_social_link7(self):
        return self.sociallink_set.get(pos=7)

    @property
    def get_social_link8(self):
        return self.sociallink_set.get(pos=8)

#Make sure we create a Profile when creating a User
def create_profile(sender, instance, created, **kwargs):
    if created and instance.password != 'legacy_user_password':
        UserProfile.objects.create(user=instance)
        instance.welcomenotification_set.create(user=instance)

post_save.connect(create_profile, sender=User)


def new_users_handler(sender, user, response, details, **kwargs):
    """If backend has returned imag url, fetch and store it in custom profile model"""
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
            profile = user.userprofile
            profile.profile_photo.save(slugify(user.username + " social") + '.jpg', ContentFile(avatar.read()))
            profile.save()

    except HTTPError:
        pass

    return False

from social_auth.signals import socialauth_registered
socialauth_registered.connect(new_users_handler, sender=None)


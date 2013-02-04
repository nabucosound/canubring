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


class SocialLink(models.Model):
    profile = models.ForeignKey('UserProfile')
    url = models.URLField(blank=True)

    def __unicode__(self):
        return self.url

    def get_domain_name(self):
        from urlparse import urlparse
        parse_result = urlparse(self.url)
        split_domain = parse_result.netloc.split('.')
        if len(split_domain) == 3:
            return split_domain[1].lower()
        else:
            return split_domain[0].lower()


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    profile_photo = models.ImageField(upload_to='profiles')
    country = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=255, blank=True)
    second_language = models.CharField(max_length=255, blank=True)
    # Imagekit specs
    square = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(135, 135)], image_field='profile_photo', format='JPEG', options={'quality': 90})
    ticket = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(30, 30)], image_field='profile_photo', format='JPEG', options={'quality': 90})
    default_img_url = '%simg/default_profile_%s.png'

    def __unicode__(self):
        return self.user.username

    def get_languages(self):
        if self.second_language:
            return " - ".join((self.language, self.second_language))
        else:
            return self.language

    @property
    def get_square_img_url(self):
        return get_img_url(self, 'square')

    @property
    def get_ticket_img_url(self):
        return get_img_url(self, 'ticket')


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


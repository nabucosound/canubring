from urllib2 import urlopen, HTTPError
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile

from social_auth.models import UserSocialAuth


class Command(BaseCommand):
    help = "Inport fb avatar pictures from legacy system users."

    def handle(self, *args, **options):
        count = 0
        for sp in UserSocialAuth.objects.all():
            count = count + 1
            url = "http://graph.facebook.com/%s/picture?type=large" % sp.uid
            profile = sp.user.userprofile
            try:
                profile.profile_photo.url
            except ValueError:
                try:
                    avatar = urlopen(url)
                except HTTPError:
                    with open("legacy_migration/csv/err_fb_avatars.txt", "a") as myfile:
                        myfile.write("%s\n" % url)
                    print '*** HTTPError', url
                    continue
                else:
                    profile.profile_photo.save(slugify(sp.user.username + " social") + '.jpg', ContentFile(avatar.read()))
                    profile.save()
            print count, url


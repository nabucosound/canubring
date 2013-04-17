import csv
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from social_auth.models import UserSocialAuth

from legacy_migration.utils import get_value, get_language
from profiles.models import ProfileCountry, UserProfile, SocialLink

class Command(BaseCommand):
    help = "Inport users from legacy system to new db schema."

    @transaction.commit_on_success
    def handle(self, *args, **options):
        """
        "uid","email","name","lastname","language","language2","created_date","last_login","facebook_id","facebook_link","twitter_link","country"
        """
        start_date = datetime.datetime.now()

        # Make sure we do not send emails
        settings.SEND_EMAIL_NOTIFICATIONS = False

        # Open csv file and initialize counter and other objects
        ifile  = open('legacy_migration/csv/users.csv', "rb")
        reader = csv.reader(ifile)
        reader.next()  # Jump header row
        count = 0
        default_profile_country = ProfileCountry.objects.latest('id')
        countries_dict = dict([(obj.name.lower(), obj) for obj in ProfileCountry.objects.all()])

        for row in reader:
            count = count + 1

            # Get or create User
            try:
                email = get_value(row[1])[:75]
            except TypeError:
                with open("legacy_migration/csv/err_users.txt", "a") as myfile:
                    myfile.write("%s\n" % repr(row))
                continue
            # suffix_num = str(User.objects.count())
            username = '%s%s' % (email.split('@', 1)[0], count)
            username = username[:30]
            password = 'legacy_user_password'
            fields = {
                    'id': count,
                    'username': username,
                    'email': email,
                    'password': password,
                    'first_name': get_value(row[2])[:30],
                    'last_name': get_value(row[3])[:30],
                    'date_joined': get_value(row[6]),
                    'last_login': get_value(row[7]) or datetime.datetime.now(),
            }
            User.objects.create(**fields)

            # Update UserProfile
            try:
                country = countries_dict[row[11].lower().strip()]
            except KeyError:
                country = default_profile_country
            fields = {
                    'id': count,
                    'user_id': count,
                    'uid': get_value(row[0]),
                    'country': country,
                    'language': get_language(row[4]),
                    'second_language': get_language(row[5]),
                    'completed': True,
            }
            UserProfile.objects.create(**fields)

            # Get or create UserSocialAuth
            if get_value(row[8]):
                fields = {
                        'user_id': count,
                        'provider': 'facebook',
                        'uid': get_value(row[8]),
                        'extra_data': '{"access_token": "faketoken" ,"expires": "5183999", "id": "%s"}' % get_value(row[8]),
                }
                try:
                    UserSocialAuth.objects.get(uid=get_value(row[8]))
                except UserSocialAuth.DoesNotExist:
                    UserSocialAuth.objects.create(**fields)

            # # Update SocialLink related objects
            SocialLink.objects.create(profile_id=count, pos=1, url=get_value(row[9]) or '')
            SocialLink.objects.create(profile_id=count, pos=2, url=get_value(row[10]) or '')
            SocialLink.objects.create(profile_id=count, pos=3)
            SocialLink.objects.create(profile_id=count, pos=4)
            SocialLink.objects.create(profile_id=count, pos=5)
            SocialLink.objects.create(profile_id=count, pos=6)
            SocialLink.objects.create(profile_id=count, pos=7)
            SocialLink.objects.create(profile_id=count, pos=8)

            print count, row[1]

        # Print total elapsed seconds
        end_date = datetime.datetime.now()
        delta = end_date - start_date
        print
        print "Total: ", delta.total_seconds(), "seconds"

        # Close csv file
        ifile.close()


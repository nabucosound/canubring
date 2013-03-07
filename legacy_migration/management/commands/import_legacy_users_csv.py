import csv
import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError

from social_auth.models import UserSocialAuth

from legacy_migration.utils import get_value, get_language
from profiles.utils import create_nb_user, UserAlreadyExists
from profiles.models import UserProfile, ProfileCountry

class Command(BaseCommand):
    help = "Inport users from legacy system to new db schema."

    def handle(self, *args, **options):
        """
        "uid","email","name","lastname","language","language2","created_date","last_login","facebook_id","facebook_link","twitter_link","country"
        """
        ifile  = open('legacy_migration/csv/users.csv', "rb")
        reader = csv.reader(ifile)
        reader.next()  # Jump header row
        count = 0
        # while count < 6480:  # Skip rows
        #     count = count + 1
        #     reader.next()
        for row in reader:
            count = count + 1
            try:
                email = get_value(row[1])[:75]
            except TypeError:
                with open("legacy_migration/csv/err_users.txt", "a") as myfile:
                    myfile.write("%s\n" % repr(row))
                continue
            fields = {
                    'email': email,
                    'password': None,
            }
            try:
                user = create_nb_user(**fields)
                user.userprofile = UserProfile.objects.create(user=user)
            except ValueError:
                with open("legacy_migration/csv/err_users.txt", "a") as myfile:
                    myfile.write("%s\n" % repr(row))
                continue
            except UserAlreadyExists:
                user = User.objects.get(email__iexact=email)
            fields = {
                    'first_name': get_value(row[2])[:30],
                    'last_name': get_value(row[3])[:30],
                    'date_joined': get_value(row[6]),
                    'last_login': get_value(row[7]) or datetime.datetime.now(),
            }
            user.__dict__.update(**fields)
            user.save()
            default_profile_country = ProfileCountry.objects.latest('id')
            try:
                country = ProfileCountry.objects.get(name__iexact=get_value(row[11]))
            except (ValueError, ProfileCountry.DoesNotExist):
                country = default_profile_country
            fields = {
                    'uid': get_value(row[0]),
                    'language': get_language(row[4]),
                    'second_language': get_language(row[5]),
                    'completed': True,
            }
            profile = user.userprofile
            profile.__dict__.update(**fields)
            profile.country = country
            profile.save()
            if get_value(row[8]):
                fields = {
                        'user': user,
                        'provider': 'facebook',
                        'uid': get_value(row[8]),
                        'extra_data': '{"access_token": "faketoken" ,"expires": "5183999", "id": "%s"}' % get_value(row[8]),
                }
                try:
                    user.social_auth.get(provider='facebook')
                except UserSocialAuth.DoesNotExist:
                    try:
                        user.social_auth.create(**fields)
                    except IntegrityError:
                        from django.db import connection
                        connection._rollback()
                        pass
            sl1 = profile.sociallink_set.get(pos=1)
            sl1.url = get_value(row[9]) or ''
            sl1.save()
            sl2 = profile.sociallink_set.get(pos=2)
            sl2.url = get_value(row[10]) or ''
            sl2.save()
            print count, row[1]
        ifile.close()


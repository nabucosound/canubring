import csv
import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from profiles.utils import create_nb_user, UserAlreadyExists
from profiles.models import UserProfile, ProfileCountry

def get_value(value):
    return None if value == '\N' else value.lower().strip()

def get_language(value):
    languages = {'eng': 1, 'spa': 2, 'por': 3, 'fra': 4}
    try:
        lang = get_value(value) and languages[get_value(value)] or 0
    except KeyError:
        lang = 0
    return lang

class Command(BaseCommand):
    help = "Inport users from legacy system to new db schema."

    def handle(self, *args, **options):
        """
        "uid","email","name","lastname","language","language2","created_date","last_login","facebook_id","facebook_link","twitter_link","country"
        """
        ifile  = open('/Users/nabuco/Desktop/users_canubring.csv', "rb")
        reader = csv.reader(ifile)
        reader.next()  # Jump header row
        count = 0
        while count < 10350:
            count = count + 1
            reader.next()
        for row in reader:
            count = count + 1
            try:
                email = get_value(row[1])[:75]
            except TypeError:
                with open("/Users/nabuco/Desktop/bad_users_canubring.txt", "a") as myfile:
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
                with open("/Users/nabuco/Desktop/bad_users_canubring.txt", "a") as myfile:
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
                    'language': get_language(row[4]),
                    'second_language': get_language(row[5]),
                    'facebook_id': get_value(row[8]),
                    'completed': True,
            }
            profile = user.userprofile
            profile.__dict__.update(**fields)
            profile.country = country
            profile.save()
            sl1 = profile.sociallink_set.get(pos=1)
            sl1.url = get_value(row[9]) or ''
            sl1.save()
            sl2 = profile.sociallink_set.get(pos=2)
            sl2.url = get_value(row[10]) or ''
            sl2.save()
            print count, row[1]
        ifile.close()


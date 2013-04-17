import csv
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from profiles.models import UserProfile
from legacy_migration.utils import get_value, get_transportation
from trips.models import Trip


class Command(BaseCommand):
    help = "Inport trips from legacy system to new db schema."

    def handle(self, *args, **options):
        """
        "uid","user_id","title","language","body","created_date","transport_type","departure_date","arrival_date","departure_city","arrival_city"
        """
        start_date = datetime.datetime.now()

        # Make sure we do not send emails
        settings.SEND_EMAIL_NOTIFICATIONS = False

        # Open csv file and initialize counter and other objects
        ifile  = open('legacy_migration/csv/trips.csv', "rb")
        reader = csv.reader(ifile)
        reader.next()  # Jump header row
        count = 0

        for row in reader:
            count = count + 1

            if len(row) < 10:
                with open("legacy_migration/csv/err_trips.txt", "a") as myfile:
                    myfile.write("%s\n" % repr(row))
                continue

            # Get User
            try:
                profile = UserProfile.objects.get(uid__iexact=get_value(row[1]))
            except (ValueError, UserProfile.DoesNotExist):
                with open("legacy_migration/csv/err_trips.txt", "a") as myfile:
                    myfile.write("%s\n" % repr(row))
                continue
            user = profile.user

            # get or create Trip
            fields = {
                    'uid': get_value(row[0]),
                    'user': user,
                    'comments': get_value(row[4]),
                    'creation_dt': get_value(row[5]),
                    'travelling_by': get_transportation(row[6]),
                    'departure_dt': get_value(row[7]) or get_value(row[8]),
                    'destination_dt': get_value(row[8]),
                    'departure_city': get_value(row[9]),
                    'destination_city': get_value(row[10]),
            }
            try:
                Trip.objects.get(uid=get_value(row[0]))
            except Trip.DoesNotExist:
                try:
                    Trip.objects.create(**fields)
                except (UnicodeDecodeError, AttributeError, ValidationError):
                    with open("legacy_migration/csv/err_trips.txt", "a") as myfile:
                        myfile.write("%s\n" % repr(row))
                    continue

            print count, row[2]

        # Print total elapsed seconds
        end_date = datetime.datetime.now()
        delta = end_date - start_date
        print
        print "Total: ", delta.total_seconds(), "seconds"

        # Close csv file
        ifile.close()


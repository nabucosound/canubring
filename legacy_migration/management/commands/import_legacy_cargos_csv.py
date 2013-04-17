import csv
import datetime

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db import DatabaseError

from profiles.models import UserProfile
from legacy_migration.utils import get_value
from trips.models import Trip
from cargos.models import Cargo, CargoComment


class Command(BaseCommand):
    help = "Inport cargos from legacy system to new db schema."

    def handle(self, *args, **options):
        """
        "uid","user_id","offer_id","offer_user_id","read_date","created_date","message"
        """
        start_date = datetime.datetime.now()

        # Open csv file and initialize counter and other objects
        ifile  = open('legacy_migration/csv/cargos.csv', "rU")
        reader = csv.reader(ifile, quotechar='"')
        reader.next()  # Jump header row
        count = 0

        for row in reader:
            count = count + 1

            # Get Trip
            try:
                trip = Trip.objects.only('uid').get(uid__iexact=get_value(row[2]))
            except (IndexError, ValueError, Trip.DoesNotExist):
                with open("legacy_migration/csv/err_cargos.txt", "a") as myfile:
                    myfile.write("%s\n" % repr(row))
                continue

            # Get User
            try:
                comment_profile = UserProfile.objects.only('uid', 'user').get(uid__iexact=get_value(row[1]))
            except UserProfile.DoesNotExist:
                with open("legacy_migration/csv/err_cargos.txt", "a") as myfile:
                    myfile.write("%s\n" % repr(row))
                continue
            comment_user = comment_profile.user

            # Get or create Cargos
            if get_value(row[1]) == get_value(row[3]):
                cargos = Cargo.objects.filter(trip__uid__iexact=get_value(row[2]))
            else:
                try:
                    cargo = Cargo.objects.get(trip__uid__iexact=get_value(row[2]), requesting_user=comment_user)
                except Cargo.DoesNotExist:
                    fields = {
                            'trip': trip,
                            'requesting_user': comment_user,
                            'traveller_user': trip.user,
                    }
                    cargo = Cargo.objects.create(**fields)
                cargos = Cargo.objects.filter(trip__uid__iexact=get_value(row[2]), requesting_user=comment_user)

            # # Get or create CargoComment
            base_fields = {
                    'uid': get_value(row[0]),
                    'user': comment_user,
                    'content': get_value(row[6]),
                    'unread': get_value(row[4]) and False or True,
                    'creation_dt': get_value(row[5]),
            }
            for cargo in cargos:
                fields = base_fields.copy()
                fields.update({'cargo': cargo,})
                try:
                    comment = CargoComment.objects.get(uid=get_value(row[0]), cargo=cargo)
                except CargoComment.DoesNotExist:
                    try:
                        pass
                        # comment = CargoComment.objects.create(**fields)
                    except (DatabaseError, UnicodeDecodeError, AttributeError, ValidationError):
                        with open("legacy_migration/csv/err_trips.txt", "a") as myfile:
                            myfile.write("%s\n" % repr(row))
                        from django.db import connection
                        connection._rollback()
                        continue

            print count, row[0]

        # Print total elapsed seconds
        end_date = datetime.datetime.now()
        delta = end_date - start_date
        print
        print "Total: ", delta.total_seconds(), "seconds"

        # Close csv file
        ifile.close()


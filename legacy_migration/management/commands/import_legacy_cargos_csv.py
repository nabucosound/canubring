import csv

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
        ifile  = open('legacy_migration/csv/cargos.csv', "rU")
        reader = csv.reader(ifile, quotechar='"')
        reader.next()  # Jump header row
        count = 0
        # while count < 10350:  # Skip rows
        #     count = count + 1
        #     reader.next()
        for row in reader:
            count = count + 1
            try:
                trip = Trip.objects.get(uid__iexact=get_value(row[2]))
            except (IndexError, ValueError, Trip.DoesNotExist):
                with open("legacy_migration/csv/err_cargos.txt", "a") as myfile:
                    myfile.write("%s\n" % repr(row))
                continue
            try:
                comment_profile = UserProfile.objects.get(uid__iexact=get_value(row[1]))
            except UserProfile.DoesNotExist:
                with open("legacy_migration/csv/err_cargos.txt", "a") as myfile:
                    myfile.write("%s\n" % repr(row))
                continue
            comment_user = comment_profile.user
            try:
                cargo = Cargo.objects.get(trip__uid__iexact=get_value(row[2]))
            except Cargo.DoesNotExist:
                fields = {
                        'trip': trip,
                        'requesting_user': trip.user,
                        'traveller_user': trip.user,
                }
                cargo = Cargo.objects.create(**fields)
            fields = {
                    'uid': get_value(row[0]),
                    'cargo': cargo,
                    'user': comment_user,
                    'content': get_value(row[6]),
                    'unread': get_value(row[4]) and True or False,
                    'creation_dt': get_value(row[5]),
            }
            try:
                comment = CargoComment.objects.get(uid=get_value(row[0]))
            except CargoComment.DoesNotExist:
                try:
                     comment = CargoComment.objects.create(**fields)
                except (DatabaseError, UnicodeDecodeError, AttributeError, ValidationError):
                    with open("legacy_migration/csv/err_trips.txt", "a") as myfile:
                        myfile.write("%s\n" % repr(row))
                    from django.db import connection
                    connection._rollback()
                    continue
                else:
                    comment.creation_dt = get_value(row[5])
                    comment.save()
            print count, row[0]
        ifile.close()
        return

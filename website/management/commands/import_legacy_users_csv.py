import csv
from django.core.management.base import BaseCommand

from profiles.utils import create_nb_user


class Command(BaseCommand):
    help = "Inport users from legacy system to new db schema."

    def handle(self, *args, **options):
        """
        "uid","email","name","lastname","language","language2","created_date","last_login","facebook_id","facebook_link","twitter_link","country"
        """
        ifile  = open('/Users/nabuco/Desktop/users_canubring.csv', "rb")
        reader = csv.reader(ifile)
        reader.next()  # Jump header row
        for row in reader:
            # if row[-4] == '\N'': row[-4] = None
            fields = {
                    'email': row[1],
                    'password': None,
            }
            user = create_nb_user(**fields)
            fields = {
                    'first_name': row[2],
                    'last_name': row[3],
                    'date_joined': row[6],
                    'last_login': row[7],
            }
            user.__dict__.update(**fields)
            user.save()
            fields = {
                    'language': row[2],
                    'second_language': row[2],
            }

        # parts = CarPhoto.objects.all()
        # parts = filter(lambda x: x.original_image.name != '', parts)
        # for obj in parts:
        #     for prop in ('square', 'thumbnail', 'vanity', 'tiny', 'gallery', 'featured'):
        #         img_obj = getattr(obj, prop)
        #         try:
        #             if not default_storage.exists(img_obj.name):
        #                 img_obj.generate(save=True)
        #                 print obj.id, img_obj.name
        #         except (IOError, AttributeError):
        #             print "!!!!!!!!!!!!!!!!!!!!!!!!!", obj.id, img_obj.name


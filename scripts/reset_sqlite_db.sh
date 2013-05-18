# -*- mode: shell-script -*-
#
# Made by Nabuco (http://nomadblue.com/).
# This script destroys and re-creates the sqlite project database.
# It applies all south migrations and, finally, creates a superuser.
#
# WARNING: you must have your project virtualenv activated and you must
# execute this script from the same path as the sqlite and manage.py files:
# ./scripts/reset_sqlite_db.sh

file="dev.db"
if [ -f "$file" ]
then
    rm $file
fi

python manage.py syncdb --noinput
python manage.py migrate --all
python manage.py cities_light --force-all
python manage.py createsuperuser --traceback


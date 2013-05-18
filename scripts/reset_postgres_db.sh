#!/bin/bash
# -*- mode: shell-script -*-
#
# Made by Nabuco (http://nomadblue.com/).
# This script destroys and re-creates the postgresql project database.
# It applies all south migrations and, finally, creates a superuser.
#
# WARNING: you must have your project virtualenv activated and you must
# execute this script from the same path as the manage.py file:
# ./scripts/reset_postgres_db.sh

dropdb canubring
createdb canubring
python manage.py syncdb --noinput
python manage.py migrate --all
python manage.py cities_light --force-all
python manage.py createsuperuser


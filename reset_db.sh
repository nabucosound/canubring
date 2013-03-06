dropdb canubring
createdb canubring
./manage.py syncdb --noinput
./manage.py migrate --all
psql canubring < profiles/sql/country.postgresql.sql
./manage.py createsuperuser


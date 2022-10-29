#!/bin/bash

python manage.py migrate
python manage.py create_superuser
python manage.py insert_countries
python manage.py insert_nps_data

python manage.py collectstatic --noinput

/usr/local/bin/gunicorn config.wsgi --bind 0.0.0.0:80 --chdir=/code
#!/bin/bash

python manage.py migrate
python manage.py create_superuser
python manage.py insert_countries
python manage.py insert_nps_data

python manage.py runserver 0.0.0.0:8000

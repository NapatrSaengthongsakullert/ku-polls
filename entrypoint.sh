#!/bin/sh

python ./manage.py migrate
python ./manage.py loaddata data/users.json
python ./manage.py loaddata data/votes-v4.json
python ./manage.py loaddata data/polls-v4.json
python ./manage.py createsuperuser --username napatr --email napatr@example.com --noinput
python ./manage.py runserver 0.0.0.0:8000


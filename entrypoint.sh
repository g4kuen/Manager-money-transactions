#!/bin/sh


until pg_isready -h db -U postgres -d transactions; do
  sleep 2
done

python manage.py migrate
python manage.py seed_db
exec "$@"
#!/bin/sh

echo "Waiting for database to be available..."
/wait-for-it.sh db:3306 --timeout=30 --strict -- echo "Database is ready."

if ! python manage.py showmigrations | grep -q ' [ ]'; then
  echo "Applying migrations..."
  python manage.py migrate
fi

if ! python manage.py loaddata site_data_latest_encoded.json; then
  echo "Loading fixture..."
  python -Xutf8 manage.py loaddata site_data_latest_encoded.json
fi

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000

exec "$@"
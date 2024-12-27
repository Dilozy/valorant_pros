#!/bin/sh

echo "Waiting for database to be available..."
/wait-for-it.sh db:3306 --timeout=30 --strict -- echo "Database is ready."


MIGRATION_FLAG="/app/.migrations_applied"

if [ -f "$MIGRATION_FLAG" ]; then
    echo "Migrations have already been applied, skipping..."
else
    echo "Migrations have not been applied. Applying migrations..."
    
    python manage.py migrate

    touch "$MIGRATION_FLAG"
    echo "Migration flag created: $MIGRATION_FLAG"
fi

FIXTURE_FLAG="/app/.fixture_loaded"

if [ -f "$FIXTURE_FLAG" ]; then
    echo "Fixture has been already loaded."
else
    echo "Loading fixture..."
    
    python -Xutf8 manage.py loaddata db.json
    
    touch "$FIXTURE_FLAG"
    echo "Fixture flag created: $FIXTURE_FLAG"
fi

echo "Checking for static files..."

if ! find /app/staticfiles -type f | grep -q .; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
else
  echo "Static files already collected."
fi

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000

exec "$@"
#!/bin/sh

echo "Waiting for database to be available..."
/wait-for-it.sh db:3306 --timeout=30 --strict -- echo "Database is ready."

# Применяем миграции, если они не были применены
if ! python manage.py showmigrations | grep -q ' [ ]'; then
  echo "Applying migrations..."
  python manage.py migrate
fi

# Загружаем данные, если это не было сделано
if ! python manage.py loaddata site_data_latest_encoded.json; then
  echo "Loading fixture..."
  python -Xutf8 manage.py loaddata site_data_latest_encoded.json
fi


echo "Checking for static files..."
# Проверяем, есть ли статические файлы
if ! find /app/staticfiles -type f | grep -q .; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
else
  echo "Static files already collected."
fi

# Запускаем Django сервер
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000

# Выполняем все переданные параметры (если они есть)
exec "$@"
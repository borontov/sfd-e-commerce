#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Checking PostgreSQL..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done
    echo "PostgreSQL started"
fi

if [ "$RUN_MIGRATIONS" = "true" ]
then
    echo "Running migrations..."
    python manage.py migrate --noinput
fi

if [ "$COLLECT_STATIC" = "true" ]
then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

exec "$@"
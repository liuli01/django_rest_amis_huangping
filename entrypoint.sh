#!/bin/bash

if [ "$APP_MODE" = "scheduler" ]; then
    echo "Starting scheduler service..."
    exec python manage.py runapscheduler
else
    echo "Starting web service..."
    exec python manage.py runserver 0.0.0.0:8000
fi

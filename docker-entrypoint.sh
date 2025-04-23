#!/bin/bash
set -e

# Wait for Redis to be ready
until redis-cli ping; do
  >&2 echo "Redis is unavailable - waiting"
  sleep 1
done

# Apply database migrations
flask db upgrade

# Start Celery worker in background if running in worker mode
if [ "$1" = "celery" ]; then
    exec celery -A app.celery worker --loglevel=info
fi

# Start the main application
exec "$@"
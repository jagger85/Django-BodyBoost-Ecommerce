#!/usr/bin/env bash
# Exit on error
set -o errexit

# Ensure PORT is set
if [ -z "$PORT" ]; then
    echo "ERROR: PORT environment variable is not set"
    exit 1
fi

echo "Starting Gunicorn on 0.0.0.0:$PORT"

# Start Gunicorn
exec uv run gunicorn bodyboost.wsgi:application \
    --bind "0.0.0.0:${PORT}" \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info


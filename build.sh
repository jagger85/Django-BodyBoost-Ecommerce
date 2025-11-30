#!/usr/bin/env bash
# Exit on error
set -o errexit

uv sync --frozen
uv sync --group production

# Install dependencies and build Tailwind CSS
npm install
npm run prod

# Convert static asset files
uv run python manage.py collectstatic --no-input

# Apply any outstanding database migrations
uv run python manage.py migrate --no-input

# Create superuser
uv run python manage.py create_superuser
#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies using uv (only production dependencies)
uv sync --frozen --group production

# Install dependencies and build Tailwind CSS
npm install
npm run prod

# Convert static asset files
uv run python manage.py collectstatic --no-input

# Prepare to migrate
uv run manage.py makemigrations

# Apply any outstanding database migrations
uv run python manage.py migrate --no-input

# Create superuser
uv run python manage.py create_superuser
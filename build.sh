#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Install dependencies and build Tailwind CSS
npm install
npm run prod

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate --no-input

# Create superuser
python manage.py create_superuser
#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Install Node.js dependencies and build Tailwind CSS
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs
npm install
npm run prod

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate auth zero
python manage.py migrate contenttypes zero
python manage.py migrate admin zero
python manage.py migrate sessions zero
python manage.py migrate --run-syncdb
python manage.py migrate
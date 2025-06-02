from django.core.management.base import BaseCommand
from accounts.models import Account
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        if Account.objects.filter(is_superadmin=True).exists():
            self.stdout.write('Superuser already exists')
            return

        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        first_name = os.environ.get('DJANGO_SUPERUSER_FIRST_NAME', 'Admin')
        last_name = os.environ.get('DJANGO_SUPERUSER_LAST_NAME', 'User')
        username = email.split('@')[0]

        try:
            superuser = Account.objects.create_superuser(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            superuser.is_active = True
            superuser.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser {email} created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}'))

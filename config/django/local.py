from .base import * # noqa

DEBUG = True
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1']) # noqa

DEV_APPS = [
    "django_browser_reload",
]

INSTALLED_APPS += DEV_APPS # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3', # noqa
    }
}
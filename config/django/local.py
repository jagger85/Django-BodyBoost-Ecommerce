from .base import *  # noqa
from .base import env

DEBUG = True
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])  # noqa

DEV_APPS = [
    "django_browser_reload",
    "storages",
]

INSTALLED_APPS += DEV_APPS  # noqa

# Add django-browser-reload middleware for development
MIDDLEWARE.insert(0, "django_browser_reload.middleware.BrowserReloadMiddleware")  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa
    }
}

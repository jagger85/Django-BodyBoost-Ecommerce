from .base import *  # noqa
from .base import env

DEBUG = False

# ALLOWED HOSTS
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["bodyboost.onrender.com"])  # noqa

# AWS SETTINGS
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")

# S3 Storage configuration
AWS_S3_FILE_OVERWRITE = False
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="eu-central-1")

STORAGES = {
    # Media file management (images)
    "default": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
    # CSS and JS file management
    "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USERNAME"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_ENDPOINT"),
        "PORT": env("DB_PORT"),
    }
}

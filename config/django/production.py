from .base import *  # noqa
import dj_database_url

DEBUG = False

# ALLOWED HOSTS
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["bodyboost.onrender.com"])  # noqa


DATABASES = {
    "default": dj_database_url.config(
        # Replace this value with your local database's connection string.
        default="postgresql://postgres:postgres@localhost:5432/bb_db",
        conn_max_age=600,
    )
}

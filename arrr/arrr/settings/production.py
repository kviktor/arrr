from .base import *  # noqa
import os


DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

ADMINS = (
    ('Kálmán Viktor', 'kviktor@...'),
)

MANAGERS = ADMINS

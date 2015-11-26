# flake8: noqa
from .base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = get_env_variable('SECRET_KEY')


ALLOWED_HOSTS = get_env_variable('DJANGO_ALLOWED_HOSTS').split(',')


ADMINS = (
    ('Kálmán Viktor', 'kviktor@...'),
)

MANAGERS = ADMINS

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = get_env_variable('EMAIL_HOST', 'localhost')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = get_env_variable('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
DEFAULT_FROM_EMAIL = get_env_variable('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = get_env_variable('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

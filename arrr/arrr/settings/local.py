from .base import *  # noqa

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = get_env_variable('DEFAULT_FROM_EMAIL', "root@localhost")

# flake8: noqa

from json import loads
from sys import path
from os import environ
from os.path import join, abspath, dirname, isfile, basename


# this is okay
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name, default=None):
    """ Get the environment variable or return exception/default """
    try:
        return environ[var_name]
    except KeyError:
        if default is None:
            error_msg = "Set the %s environment variable" % var_name
            raise ImproperlyConfigured(error_msg)
        else:
            return default


BASE_DIR = dirname(dirname(abspath(__file__)))

SITE_ROOT = dirname(BASE_DIR)

SITE_NAME = basename(BASE_DIR)

DJANGO_URL = get_env_variable("DJANGO_URL", "http://localhost:8085/")


path.append(BASE_DIR)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CHANGE THIS!!!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'arrr.urls'


DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
)

THIRD_PARTY_APPS = (
    'crispy_forms',
    'crispy_forms_foundation',
)

LOCAL_APPS = ("arrr", )

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'arrr.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(SITE_ROOT, 'arrr.db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'  # 'Europe/London'

USE_I18N = True

# this is stronger than DATETIME_INPUT_FORMATS
USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = join(SITE_ROOT, 'media')
MEDIA_URL = '/media/'

# Additional locations of static files

STATICFILES_DIRS = (
    join(SITE_ROOT, 'arrr', 'static'),
)

TEMPLATE_DIRS = (
    join(SITE_ROOT, 'arrr', 'templates'),
)

# Add 'foundation-5' layout pack
CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap', 'uni_form', 'bootstrap3', 'foundation-5')
# Default layout to use with "crispy_forms"
CRISPY_TEMPLATE_PACK = 'foundation-5'

DATETIME_INPUT_FORMATS = (
    "%Y-%m-%d %H:%M",
)

DATETIME_FORMAT = "Y-m-d H:i"

LOGIN_REDIRECT_URL = "/"


# SAML2
if get_env_variable('DJANGO_SAML', 'FALSE') == 'TRUE':
    from shutil import which
    from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT

    INSTALLED_APPS += (
        "djangosaml2",
    )
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'djangosaml2.backends.Saml2Backend',
    )

    remote_metadata = join(SITE_ROOT, 'remote_metadata.xml')
    if not isfile(remote_metadata):
        raise ImproperlyConfigured('Download SAML2 metadata to %s' %
                                   remote_metadata)
    required_attrs = loads(get_env_variable('DJANGO_SAML_REQUIRED',
                                            '["uid"]'))
    optional_attrs = loads(get_env_variable('DJANGO_SAML_OPTIONAL',
                                            '["mail", "cn", "sn"]'))

    SAML_CONFIG = {
        'xmlsec_binary': which('xmlsec1'),
        'entityid': DJANGO_URL + 'saml2/metadata',
        'attribute_map_dir': join(SITE_ROOT, 'attribute-maps'),
        'service': {
            'sp': {
                'name': SITE_NAME,
                'endpoints': {
                    'assertion_consumer_service': [
                        (DJANGO_URL + 'saml2/acs/', BINDING_HTTP_POST),
                    ],
                    'single_logout_service': [
                        (DJANGO_URL + 'saml2/ls/', BINDING_HTTP_REDIRECT),
                    ],
                },
                'required_attributes': required_attrs,
                'optional_attributes': optional_attrs,
            },
        },
        'metadata': {'local': [remote_metadata], },
        'key_file': join(SITE_ROOT, 'samlcert.key'),  # private part
        'cert_file': join(SITE_ROOT, 'samlcert.pem'),  # public part
        'encryption_keypairs': [
            {
                'key_file': join(SITE_ROOT, 'samlcert.key'),
                'cert_file': join(SITE_ROOT, 'samlcert.pem'),
            }
        ],
        'encryption_keypairs': [
            {
                'key_file': join(SITE_ROOT, 'samlcert.key'),
                'cert_file': join(SITE_ROOT, 'samlcert.pem'),
            }
        ]
    }

    try:
        SAML_CONFIG += loads(get_env_variable('DJANGO_SAML_SETTINGS'))
    except ImproperlyConfigured:
        pass

    SAML_CREATE_UNKNOWN_USER = True
    SAML_ATTRIBUTE_MAPPING = loads(get_env_variable(
        'DJANGO_SAML_ATTRIBUTE_MAPPING',
        '{"mail": ["email"], "sn": ["last_name"], '
        '"uid": ["username"], "cn": ["first_name"]}'))

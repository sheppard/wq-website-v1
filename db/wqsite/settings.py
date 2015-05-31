"""
Django settings for wqsite project.
Based on the Django 1.6 template, with wq-specific modifications noted as such

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/

For more information about wq.db's Django settings see
http://wq.io/docs/settings

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# wq: extra dirname() to account for db/ folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# wq: SECRET_KEY, DEBUG and TEMPLATE_DEBUG are defined in local_settings.py

ALLOWED_HOSTS = ["wq.io"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',

    'rest_framework',

    'wq.db.patterns.annotate',
    'wq.db.patterns.identify',
    'wq.db.patterns.relate',
    'wq.db.patterns.locate',
    'wq.db.patterns.mark',
    'wq.db.rest',
    'wq.db.rest.auth',

    'wq.db.contrib.files',

    'content',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wqsite.middleware.DocVersionMiddleware',
)

# wq: Recommended settings for Django, rest_framework, and social auth
from wq.db.default_settings import (
    TEMPLATE_LOADERS,
    TEMPLATE_CONTEXT_PROCESSORS,
    SESSION_COOKIE_HTTPONLY,
    REST_FRAMEWORK,
    SOCIAL_AUTH_PIPELINE,
)
TEMPLATE_CONTEXT_PROCESSORS += (
    "content.context_processors.menu",
)
REST_FRAMEWORK['UPLOADED_FILES_USE_URL'] = False

# wq: Recommended settings unique to wq.db
from wq.db.default_settings import (
    ANONYMOUS_PERMISSIONS,
    SRID,
    DEFAULT_AUTH_GROUP,
)

ROOT_URLCONF = "wqsite.urls"

WSGI_APPLICATION = 'wqsite.wqsgi'


WQ_MARKDOWNTYPE_MODEL = 'content.MarkdownType'
MARKDOWN_EXTENSIONS = ['fenced_code', 'tables']


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# wq: DATABASES is defined in local_settings.py

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# wq: Configure paths for default project layout
STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DOCS_ROOT = os.path.join(BASE_DIR, 'wq', 'docs')
VERSION_TXT = os.path.join(BASE_DIR, 'version.txt')
MEDIA_URL = '/media/'
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# wq: Import local settings
try:
    from .local_settings import *
except ImportError:
    pass

from wq.app.build import collect
CONF = collect.readfiles(os.path.join(BASE_DIR, 'conf'), 'yaml', 'yml')

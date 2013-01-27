# Settings for canubring project
import os

def bool_env(val):
    """Replaces string based environment values with Python booleans"""
    return True if os.environ.get(val, False) == 'True' else False

DEBUG = bool_env('DEBUG')
TEMPLATE_DEBUG = DEBUG

LANGUAGE_CODE = 'en'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = False

SITE_ID = 1

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'yc)21v(bd3y1qe1kv74khyar962m15+awbv#a3z0!y58cvy5ld'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'canubring.urls'

WSGI_APPLICATION = 'canubring.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'gunicorn',
    'south',
    'django_extensions',
    # 'django_facebook',
    'imagekit',
    'django_ses',
    'storages',
    'website',
    'search',
    'profiles',
    'trips',
)

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

TEMPLATE_CONTEXT_PROCESSORS = (
    # 'django_facebook.context_processors.facebook',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

# Database
import dj_database_url
DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}

# Auth
# AUTH_PROFILE_MODULE = 'profiles.Profile'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# Registration & authentication
# FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
# FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')
# FACEBOOK_LOGIN_DEFAULT_REDIRECT = '/'
# FACEBOOK_HIDE_CONNECT_TEST = True
# FACEBOOK_CELERY_STORE = False
# FACEBOOK_CELERY_TOKEN_EXTEND = False
# FACEBOOK_STORE_LIKES = True
# FACEBOOK_STORE_FRIENDS = True
# FACEBOOK_DEFAULT_SCOPE = ['email', 'user_birthday', 'publish_actions']

# Amazon keys
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Amazon SES
EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL = 'info@canubring.com'

# Amazon S3
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '/media/'
STATIC_URL = S3_URL

# Imagekit
IMAGEKIT_DEFAULT_IMAGE_CACHE_BACKEND = 'imagekit.imagecache.NonValidatingImageCacheBackend'

# Debug toolbar
INTERNAL_IPS = ('127.0.0.1',)

# Test deployment on Ubuntu uses it. Heroku and Foreman use .env conf file.
try:
    from canubring.localsettings import *
except:
    pass

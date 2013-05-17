import os

def env_var(key, default=None):
    """Retrieves env vars and makes Python boolean replacements"""
    val = os.environ.get(key, default)
    if val == 'True': val = True
    elif val == 'False': val = False
    return val

# Debug
INTERNAL_IPS = ('127.0.0.1',)
DEBUG = env_var('DEBUG', True)
TEMPLATE_DEBUG = DEBUG

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Chicago'
SITE_ID = 1

USE_TZ = False
USE_I18N = True
USE_L10N = True

ugettext = lambda s: s
LANGUAGES = (
    ('en', ugettext('English')),
    ('es', ugettext('Spanish')),
    ('pt', ugettext('Portuguese')),
)
SETTINGS_FILE_ROOT = os.path.dirname(os.path.realpath(__file__))
LOCALE_PATHS = (
        os.path.join(SETTINGS_FILE_ROOT, '..', 'locale'),
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'profiles.middleware.CompleteRegistration',
)

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
    'imagekit',
    'django_ses',
    'storages',
    'cities_light',
    'website',
    'search',
    'profiles',
    'trips',
    'social_auth',
    'cargos',
    'legacy_migration',
    'notifier',
    'notifications',
    'password_reset',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    # Social auth
    # 'social_auth.context_processors.social_auth_by_name_backends',
    # 'social_auth.context_processors.social_auth_backends',
    # 'social_auth.context_processors.social_auth_by_type_backends',
    # 'social_auth.context_processors.social_auth_login_redirect',
)

ROOT_URLCONF = 'prj.urls'
WSGI_APPLICATION = 'prj.wsgi.application'
ALLOWED_HOSTS = env_var('ALLOWED_HOSTS', '*').split(',')
SECRET_KEY = env_var('SECRET_KEY', 'your$%&/defaultsecretkeygoesheremyfriend!')

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

# Database
import dj_database_url
DATABASES = {'default': dj_database_url.config(default=env_var('DATABASE_URL'))}

# Django Admin
ADMIN_URL = env_var('ADMIN_URL', 'admin/')

# Social auth
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL          = '/'
LOGIN_REDIRECT_URL = '/my/profile/'
LOGIN_ERROR_URL    = '/'
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_API_SECRET = os.environ.get('FACEBOOK_APP_SECRET')
FACEBOOK_EXTENDED_PERMISSIONS = ['email', 'publish_actions']
GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')
LINKEDIN_CONSUMER_KEY = os.environ.get('LINKEDIN_CONSUMER_KEY')
LINKEDIN_CONSUMER_SECRET = os.environ.get('LINKEDIN_CONSUMER_SECRET')
LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress',]
LINKEDIN_EXTRA_FIELD_SELECTORS = ['email-address', 'headline', 'industry', 'picture-url']
LINKEDIN_EXTRA_DATA = [('id', 'id'),
                       ('first-name', 'first_name'),
                       ('last-name', 'last_name'),
                       ('email-address', 'email_address'),
                       ('picture-url', 'picture_url'),
                       ('headline', 'headline'),
                       ('industry', 'industry')]

# Amazon keys
AWS_ACCESS_KEY_ID = env_var('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env_var('AWS_SECRET_ACCESS_KEY')

# Amazon S3
AWS_STORAGE_BUCKET_NAME = env_var('AWS_STORAGE_BUCKET_NAME')
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '/media/'
STATIC_URL = S3_URL

# Amazon SES
EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL = env_var('DEFAULT_FROM_EMAIL')
DEFAULT_FROM_HEADER = 'Canubring'
SEND_EMAIL_NOTIFICATIONS = env_var('SEND_EMAIL_NOTIFICATIONS', False)

# Imagekit backend that DOES NOT TRY to generate img if
# filepath exists but physical file does not
IMAGEKIT_DEFAULT_IMAGE_CACHE_BACKEND = 'imagekit.imagecache.NonValidatingImageCacheBackend'

# Sometimes production db copies in local miss image paths
USE_DEFAULT_IMAGES = env_var('USE_DEFAULT_IMAGES', False)

# Google Analytics
GOOGLE_ANALYTICS_PROPERTY_ID = env_var('GOOGLE_ANALYTICS_PROPERTY_ID', False)
GOOGLE_ANALYTICS_DOMAIN = env_var('GOOGLE_ANALYTICS_DOMAIN', False)

# Flags to enable/disable features
ENABLE_DEBUG_TOOLBAR = env_var('ENABLE_DEBUG_TOOLBAR', False)
LOCAL_STORAGE = env_var('LOCAL_STORAGE', False)

# Test deployment on Ubuntu uses it. Heroku and Foreman use .env conf file.
try:
    from prj.localsettings import *
except:
    pass


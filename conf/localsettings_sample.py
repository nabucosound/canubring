from settings import env_var

############ BEGIN -- Edit your settings ###
# WARNING: The full path MUST exist, so create it if it doesn't
STATIC_CONTAINER_PATH = '/path/to/prj_static/prj_name/'
MEDIA_CONTAINER_PATH = '/path/to/prj_media/prj_name/'
############ END -- No need to edit anything more below this section ###

# Fallback to default storage and media serve from local filesystem
if env_var('LOCAL_STORAGE', False):
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    STATIC_ROOT = STATIC_CONTAINER_PATH
    MEDIA_ROOT = MEDIA_CONTAINER_PATH
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    IMAGEKIT_DEFAULT_IMAGE_CACHE_BACKEND = 'imagekit.imagecache.PessimisticImageCacheBackend'

# Django debug toolbar
if env_var('ENABLE_DEBUG_TOOLBAR', False):
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        from settings import MIDDLEWARE_CLASSES, INSTALLED_APPS
        INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
        INTERNAL_IPS = ('127.0.0.1',)
        DEBUG_TOOLBAR_CONFIG = {
            'INTERCEPT_REDIRECTS': False,
        }


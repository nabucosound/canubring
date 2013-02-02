from django.conf import settings


def get_img_url(obj, attr_name, url=None):
    """``url`` param is the default url string to return if image file does not exist"""
    if url is None:
        url = obj.default_img_url
    url = url % (settings.STATIC_URL, attr_name)
    if not getattr(settings, 'USE_DEFAULT_IMAGES', False):
        try:
            attr = getattr(obj, attr_name)
            url = attr.url
        except (AttributeError, ValueError):
            pass
    return url


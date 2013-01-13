import re
from django import template

register = template.Library()

@register.simple_tag
def active_nav_menu_item(request, pattern):
    if re.search("^%s$" % pattern, request.path):
        return 'active'
    return ''


import re
from django import template
from cargos.models import Currency


register = template.Library()

@register.simple_tag
def active_nav_menu_item(request, pattern):
    if re.search("^%s$" % pattern, request.path):
        return 'active'
    return ''

@register.assignment_tag
def get_currencies():
    return Currency.objects.order_by('id')


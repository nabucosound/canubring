from django import template


register = template.Library()

@register.filter
def is_unread(obj, user):
    return obj.unread and obj.user != user



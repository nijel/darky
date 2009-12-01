from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def msgtype(value):
    return value.split('::', 1)[0]

@register.filter
@stringfilter
def msgtext(value):
    return value.split('::', 1)[1]


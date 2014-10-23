from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.inclusion_tag('message.html')
def show_message(tags, message):
    return {
        'tags': tags,
        'message': message,
    }

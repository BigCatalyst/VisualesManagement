from django import template
from music.models import DVD, Album

register = template.Library()


@register.filter(is_safe=True)
def isinstance_dvd(value):
    return isinstance(value, DVD)


@register.filter(is_safe=True)
def isinstance_album(value):
    return isinstance(value, Album)

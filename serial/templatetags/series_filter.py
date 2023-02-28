from django import template
from django.db.models import Count
from django.template.defaultfilters import stringfilter
from serial.models import Season, Serial

register = template.Library()


@register.filter
def first_season_year(value: Season.objects):
    """
    Returns the last word for a given string
    """
    seasons = value.values_list("number", flat=True)
    if seasons:
        first_season = sorted(seasons, key=lambda x: int(x))[0]
        return value.filter(number=first_season).first().year


@register.filter
def last_season_year(value: Season.objects):
    """
    Returns the last word for a given string
    """
    seasons = value.values_list("number", flat=True)
    if seasons:
        last_season = sorted(seasons, key=lambda x: int(x))[-1]
        return value.filter(number=last_season).first().year


@register.filter(is_safe=True)
@stringfilter
def split(value, arg):
    return value.split(arg)

    
@register.filter
def definition(serial: Serial):
    """
    Returns the last word for a given string
    """
    queryset = Season.objects.filter(series_id=serial.id).values("definition").annotate(count=Count("definition")).order_by("-definition").exclude(definition__icontains="No").exclude(definition=None)
    if queryset:
        return "/".join([item["definition"] for item in queryset])
    else:
        return False

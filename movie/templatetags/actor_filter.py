from django import template
from django.db.models import Sum, IntegerField
from django.db.models.functions import Cast
from django.core.files.storage import default_storage
from django.template.defaultfilters import stringfilter


from movie.models import Documental

register = template.Library()


@register.filter
def last_word(value):
    """
    Returns the last word for a given string
    """
    return value.split()[-1]


@register.filter(is_safe=True, name="Zip")
def as_Zip(results, objects):
    return zip(results, objects)

@register.filter
def without3d(actor):
    return actor.movie_set.exclude(format__format__iexact="3d").order_by("title_eng")

@register.filter
def ordermovie(saga):
    return saga.movie_set.all().order_by("-year")


@register.filter(name='file_exists')
def file_exists(filepath):
    if default_storage.exists("media/" + str(filepath)):
        return True
    else:
        return False


@register.filter(name='mod')
def mod(n, value):
    return n % int(value)


@register.filter(name='next_mod')
def mod_plus(n, value):
    return (int(n)+1) % int(value)


@register.filter(name='first_image')
def saga_image(movie_set):
    for movie in movie_set.all():
        print(movie)
        if movie.photo is not None or movie.photo != '':
            print(movie.photo)
            print("-------------")
            print(movie.photo.url)
            return movie.photo.url
    return None
    

@register.filter(name='episodes')
def doc(movie):
    m = Documental.objects.filter(id=movie.id).first()
    total = 0
    for season in m.documentalseason_set.all():
        total += int(season.chapters.split(" ")[0])
    #return m.aggregate(episodes=Sum(Cast("documentalseason__chapters", output_field=IntegerField())))["episodes"]
    return total
    
@register.filter
@stringfilter
def trim(value):
    return value.strip().rstrip()


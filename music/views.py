from django.db.models.expressions import Func, F, Value
from django.db.models.fields import IntegerField, FloatField
from django.db.models import Q, Avg, Case, When
from django.db.models.functions import Cast
from django.shortcuts import render
from django.views.generic import DetailView
from music.models import DVD, Album, Author, Collection, Concert, GenderMusic
from django.views.decorators.cache import cache_page

@cache_page(60 * 1440)
def music_page(request):
    if not request.GET.get("q") or not request.GET.get("init"):
        return render(request, template_name="pages/music.html")
    elif request.GET.get("q") == "concierto" and request.GET.get("init"):
        initial = (
            f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
            if request.GET.get("init") != "no"
            else "^[0-9]"
        )
        concerts = Concert.objects.filter(interpreter__regex=initial).all()
        
        if "search" in request.GET:
            search_term = request.GET.get("search", "")
            concerts = Concert.objects.all().annotate(
                k1=Case(
                    When(interpreter__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(interpreter__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                
                rank=F("k1") + F("k2"),
                
            ).exclude(rank=0.0).distinct().order_by("-rank", "interpreter")
            return render(
                request,
                template_name="pages/music_filter.html",
                context={"movies": concerts},
            )
        
        if request.GET.get("init") == "no":
            concerts = concerts.annotate(my_integer_field=Cast(Func(F(
                'interpreter'), Value('[^\d]'), Value(''), Value('g'),
                function='regexp_replace'), IntegerField())).order_by(
                "my_integer_field", "interpreter")
        return render(
            request,
            template_name="pages/music_filter.html",
            context={"movies": concerts},
        )
    elif request.GET.get("q") == "dvd" and request.GET.get("init"):
        initial = (
            f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
            if request.GET.get("init") != "no"
            else "^[0-9]"
        )
        dvds = DVD.objects.filter(author__name__regex=initial).all()
        if "search" in request.GET:
            search_term = request.GET.get("q", "")
            dvds = DVD.objects.all().annotate(
                k1=Case(
                    When(title__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(title__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k3=Case(
                    When(author__name__istartswith=search_term, then=Value(1)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k4=Case(
                    When(author__name__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                
                rank=F("k1") + F("k2"),
                rank2=F("k3") + F("k4")
            ).exclude(rank=0.0, rank2=0.0).distinct().order_by("-rank", "-rank2", "title")
            return render(
                request,
                template_name="pages/music_filter.html",
                context={"movies": dvds},
            )
        if request.GET.get("init") == "no":
            dvds = dvds.annotate(my_integer_field=Cast(Func(F(
                'author__name'), Value('[^\d]'), Value(''), Value('g'),
                function='regexp_replace'), IntegerField())).order_by(
                "my_integer_field", "author__name")
        return render(
            request,
            template_name="pages/music_filter.html",
            context={"movies": dvds},
        )
    else:
        initial = (
            f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
            if request.GET.get("init") != "no"
            else "^[0-9]"
        )
        albums = Author.objects.filter(dvd=None).filter(name__regex=initial).all()
        if "search" in request.GET:
            search_term = request.GET.get("search", "")
            albums = Author.objects.filter(dvd=None).all().annotate(
                k1=Case(
                    When(name__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(name__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                
                rank=F("k1") + F("k2"),
                
            ).exclude(rank=0.0).distinct().order_by("-rank", "name")
            return render(
                request,
                template_name="pages/music_filter.html",
                context={"movies": albums},
            )
        if request.GET.get("init") == "no":
            albums = albums.annotate(my_integer_field=Cast(Func(F(
                'name'), Value('[^\d]'), Value(''), Value('g'),
                function='regexp_replace'), IntegerField())).order_by(
                "my_integer_field", "name")
        return render(
            request,
            template_name="pages/music_filter.html",
            context={"movies": albums},
        )

@cache_page(60 * 1440)
def music_gender_page(request):
    if not request.GET.get("q"):
        genders = (
            GenderMusic.objects.exclude(name__in=["Mísica del Mundo", "Sin definir"]).order_by("name").all()
        )
        print(genders)
        return render(
            request,
            template_name="pages/music_gender.html",
            context={"genders": genders},
        )
    else:
        indices = [i for i, x in enumerate(request.GET.get("q")) if x == "-"]
        gender = request.GET.get("q").replace("-", " ").title()
        new_gender = gender
        for x in indices:
            new_gender = new_gender[:x] + "-" + new_gender[x+1:]
        gender = new_gender
        initial = (
            f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
            if "init" in request.GET and request.GET.get("init") != "no"
            else "^[0-9]"
        )
        if "search" in request.GET:
            search_term = request.GET.get("search", "")
            movies = (
                Collection.objects.filter(gender__name__icontains=gender)
                .all().annotate(
                    k1=Case(
                        When(name__istartswith=search_term, then=Value(1.0)),
                        default=Value(0.0),
                        output_field=FloatField(),
                    ),
                    k2=Case(
                        When(name__icontains=search_term, then=Value(0.5)),
                        default=Value(0.0),
                        output_field=FloatField(),
                    ),
                    
                    rank=F("k1") + F("k2"),
                    
                ).exclude(rank=0.0).distinct().order_by("-rank", "name")
            )
            return render(
                request,
                template_name="pages/music_filter_gender.html",
                context={"movies": movies},
            )
        movies = (
            Collection.objects.filter(gender__name__icontains=gender)
            .filter(name__regex=initial)
            .all()
        )
        if request.GET.get("init") == "no":
            movies = movies.annotate(my_integer_field=Cast(Func(F(
                'name'), Value('[^\d]'), Value(''), Value('g'),
                function='regexp_replace'), IntegerField())).order_by(
                "my_integer_field", "name")
        
        return render(
            request,
            template_name="pages/music_filter_gender.html",
            context={"movies": movies},
        )


class CollectionDetail(DetailView):
    model = Collection
    template_name = "pages/colecction_details.html"


class ConcertDetail(DetailView):
    model = Concert
    template_name = "pages/concert_details.html"


class DVDDetail(DetailView):
    model = DVD
    template_name = "pages/disco_details.html"


class AlbumDetail(DetailView):
    model = Album
    template_name = "pages/disco_details.html"


class AuthorDetail(DetailView):
    model = Author
    template_name = "pages/author_details.html"

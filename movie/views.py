import re
from django.db.models.expressions import Func, F, Value
from django.db.models.fields import IntegerField, FloatField
from django.db.models import Q, Avg, Case, When
from django.db.models.functions import Cast
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from actor.models import Actor
from movie.models import (
    Combo,
    Documental,
    Gender,
    GenderDocumental,
    Humor,
    Movie,
    Sagas,
    Sport,
)
from serial.models import Serial
from tasks.views import load_data_2, load_data_3, load_data_1
from tasks.models import Contact

class HomeView(TemplateView):
    template_name = "pages/home.html"
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        try:
            context["object"] = Contact.objects.get(id=1)
            context["contact"] = Contact.objects.get(id=1)
        except:
            context["object"] =None
            context["contact"]=None
        return context

@cache_page(60 * 1440)
def movies_page(request):
    if "search" in request.GET and not request.GET.get("q"):
        search_term = request.GET.get("search", "")
        movies = Movie.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).exclude(
                gender__name__in=["Manga", "Animado"]).exclude(format__format__iexact="3d").order_by("title_eng")
        movies = movies.annotate(
                k1=Case(
                    When(title_eng__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(title_eng__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k3=Case(
                    When(title__istartswith=search_term, then=Value(1)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k4=Case(
                    When(title__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                rank=F("k1") + F("k2"),
                rank2=F("k3") + F("k4"),
                
            ).exclude(rank=0.0, rank2=0.0).distinct().order_by("-rank", "-rank2", "title_eng")
        return render(
            request,
            template_name="pages/movies_filter.html",
            context={"movies": movies},
        )    
    elif "search" in request.GET and request.GET.get("q") == "3d":
        q = request.GET.get("q").replace("-", " ").title()

        search_term = request.GET.get("search", "")
        movies = Movie.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).filter(format__format__iexact="3d").order_by("title_eng")
        
        movies = movies.annotate(
                k1=Case(
                    When(title_eng__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(title_eng__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k3=Case(
                    When(title__istartswith=search_term, then=Value(1)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k4=Case(
                    When(title__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                rank=F("k1") + F("k2"),
                rank2=F("k3") + F("k4"),
                
            ).exclude(rank=0.0, rank2=0.0).distinct().order_by("-rank", "-rank2", "title_eng")
        return render(
            request,
            template_name="pages/movies_filter.html",
            context={"movies": movies},
        )    
    if not request.GET.get("init"):
        return render(request, template_name="pages/movies.html")
    else:
        initial = (
            f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
            if request.GET.get("init") != "no"
            else "^[0-9]"
        )
        if request.GET.get("q") and request.GET.get("q") == "saga":
            movies = Sagas.objects.exclude(movie__gender__name="Animado").filter(title__regex=initial).all()
            if request.GET.get("init") == "no":
                movies = movies.annotate(my_integer_field=Cast(Func(F(
                    'title'), Value('[^\d]'), Value(''), Value('g'),
                    function='regexp_replace'), IntegerField())).order_by(
                    "my_integer_field", "title")
                movies = sorted(movies, key=lambda x: int(re.search(r'\d+', x.title.strip()).group()), reverse=False)
            return render(
                request,
                template_name="pages/movies_by_saga.html",
                context={"movies": movies},
            )
        elif request.GET.get("q") and request.GET.get("q") == "combo":
            movies = Combo.objects.filter(name__regex=initial).all()
            if request.GET.get("init") == "no":
                movies = movies.annotate(my_integer_field=Cast(Func(F(
                    'name'), Value('[^\d]'), Value(''), Value('g'),
                    function='regexp_replace'), IntegerField())).order_by(
                    "my_integer_field", "name")
                movies = sorted(movies, key=lambda x: int(re.search(r'\d+', x.name.strip()).group()), reverse=False)
            return render(
                request,
                template_name="pages/movies_by_combo.html",
                context={"movies": movies},
            )
        elif request.GET.get("q") and request.GET.get("q") == "sagas animadas":
            movies_list = (
                Movie.objects.exclude(saga=None)
                    .filter(gender__name="Animado")
                    .values_list("saga__id", flat=True).order_by("title_eng")
            )
            try:
                movies = (
                    Sagas.objects.filter(id__in=list(movies_list))
                        .filter(title__regex=initial)
                        .all().order_by("title_eng")
                )
            except:
                movies = (
                    Sagas.objects.filter(id__in=list(movies_list))
                        .filter(title__regex=initial)
                        .all().order_by("title")
                )
            if request.GET.get("init") == "no":
                movies = movies.annotate(my_integer_field=Cast(Func(F(
                    'title'), Value('[^\d]'), Value(''), Value('g'),
                    function='regexp_replace'), IntegerField())).order_by(
                    "my_integer_field", "title")
                movies = sorted(movies, key=lambda x: int(re.search(r'\d+', x.title.strip()).group()), reverse=False)
            return render(
                request,
                template_name="pages/movies_by_saga.html",
                context={"movies": movies},
            )
        elif request.GET.get("q") and request.GET.get("q") == "3d":            
            movies = (
                Movie.objects.filter(format__format__iexact="3d")
                    .filter(title_eng__regex=initial)
                    .all().order_by("title_eng")
            )
            if request.GET.get("init") == "no":
                movies = movies.annotate(my_integer_field=Cast(Func(F(
                    'title_eng'), Value('[^\d]'), Value(''), Value('g'),
                    function='regexp_replace'), IntegerField())).order_by(
                    "my_integer_field", "title_eng")
                movies = sorted(movies, key=lambda x: int(re.search(r'\d+', x.title_eng.strip()).group()), reverse=False)
        else:
            movies = Movie.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).exclude(
                gender__name__in=["Manga", "Animado"]).exclude(format__format__iexact="3d").filter(
                title_eng__regex=initial).all().order_by("title_eng")
        
            if request.GET.get("init") == "no":
                movies = movies.annotate(my_integer_field=Cast(Func(F(
                    'title_eng'), Value('[^\d]'), Value(''), Value('g'),
                    function='regexp_replace'), IntegerField())).order_by(
                    "my_integer_field", "title_eng")
                movies = sorted(movies, key=lambda x: int(re.search(r'\d+', x.title_eng.strip()).group()), reverse=False)
        return render(
            request,
            template_name="pages/movies_filter.html",
            context={"movies": movies},
        )

@cache_page(60 * 1440)
def sports_page(request):
    if request.GET.get("init"):
        initial = (
            f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
            if request.GET.get("init") != "no"
            else "^[0-9]"
        )
        sports = Sport.objects.filter(name__regex=initial).all()
        return render(
            request,
            template_name="pages/sport_filter.html",
            context={"movies": sports},
        )
    return render(request, template_name="pages/sports.html")


class SportDetails(DetailView):
    model = Sport
    template_name = "pages/sports_details.html"

@cache_page(60 * 1440)
def animados_page(request):
    return render(request, template_name="pages/animados.html")

@cache_page(60 * 1440)
def cinemateca_page(request):
    if not request.GET.get("init") and not request.GET.get("q"):
        return render(request, template_name="pages/cinemateca.html")
    else:
        doc_type = request.GET.get("q").title()
        initial = (
            f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
            if request.GET.get("init") != "no"
            else "^[0-9]"
        )
        if doc_type == "Humor Cubano":
            movies = Humor.objects.filter(Q(origen="Cuba") | Q(origen="CU")).filter(
                title_eng__regex=initial
            )
        elif doc_type == "Películas Cubanas":
            movies = Movie.objects.filter(Q(origen="Cuba") | Q(origen="CU")).filter(
                title_eng__regex=initial
            )
        elif doc_type == "Series Cubanas":
            movies = Serial.objects.filter(Q(origen="Cuba") | Q(origen="CU")).filter(
                title_eng__regex=initial
            )
        elif doc_type == "Documentales Cubanos":
            movies = Documental.objects.filter(Q(origen="Cuba") | Q(origen="CU")).filter(
                title_eng__regex=initial
            )
        else:
            return render(request, template_name="pages/cinemateca.html")
        if request.GET.get("init") == "no":
            movies = movies.annotate(my_integer_field=Cast(Func(F(
                'title_eng'), Value('[^\d]'), Value(''), Value('g'),
                function='regexp_replace'), IntegerField())).order_by(
                "my_integer_field", "title_eng")
            movies = sorted(movies, key=lambda x: int(re.search(r'\d+', x.title_eng.strip()).group()), reverse=False)
        return render(
            request,
            template_name="pages/cinemateca_filter.html",
            context={"movies": movies},
        )

@cache_page(60 * 1440)
def documental_page(request):
    if not request.GET.get("init"):
        return render(request, template_name="pages/documental.html")
    else:
        doc_type = request.GET.get("q").title()
        initial = (
            f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
            if request.GET.get("init") != "no"
            else "^[0-9]"
        )
        if doc_type == "Documental Puro":
            movies = (
                Documental.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).filter(type__in=[doc_type, "Serie Documental"])
                    .filter(title_eng__regex=initial)
                    .all()
            )
        else:
            movies = (
                Documental.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).filter(type=doc_type)
                    .filter(title_eng__regex=initial)
                    .all()
            )
        if request.GET.get("init") == "no":
            movies = movies.annotate(my_integer_field=Cast(Func(F(
                'title_eng'), Value('[^\d]'), Value(''), Value('g'),
                function='regexp_replace'), IntegerField())).order_by(
                "my_integer_field", "title_eng")
            movies = sorted(movies, key=lambda x: int(re.search(r'\d+', x.title_eng.strip()).group()), reverse=False)
        return render(
            request,
            template_name="pages/documental_filter.html",
            context={"movies": movies},
        )

@cache_page(60 * 1440)
def documental_gender_page(request):
    if not request.GET.get("q"):
        genders = GenderDocumental.objects.all()
        return render(
            request,
            template_name="pages/documental_gender.html",
            context={"genders": genders},
        )

    else:
        gender = request.GET.get("q").title()
        initial = (
            f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
            if request.GET.get("init") and request.GET.get("init") != "no"
            else "^[0-9]"
        )
        if gender == "Documental Puro":
            movies = (
                Documental.objects.exclude(Q(type__iexact="Película Documental") | Q(type__iexact="Pelicula Documental")).exclude(Q(type__iexact="Serie Reality Show")).exclude(Q(origen="Cuba") | Q(origen="CU")).filter(gender__type__in=[gender, "Serie Documental"])
                    .filter(title_eng__regex=initial)
                    .all()
            )
        else:
            movies = (
                Documental.objects.exclude(Q(type__iexact="Película Documental") | Q(type__iexact="Pelicula Documental")).exclude(Q(type__iexact="Serie Reality Show")).exclude(Q(origen="Cuba") | Q(origen="CU")).filter(gender__type=gender)
                    .all()
            )
        if request.GET.get("init") == "no":
            movies = movies.annotate(my_integer_field=Cast(Func(F(
                'title_eng'), Value('[^\d]'), Value(''), Value('g'),
                function='regexp_replace'), IntegerField())).order_by(
                "my_integer_field", "title_eng")
            movies = sorted(movies, key=lambda x: int(re.search(r'\d+', x.title_eng.strip()).group()), reverse=False)
        return render(
            request,
            template_name="pages/documental_filter.html",
            context={"movies": movies},
        )

@cache_page(60 * 1440)
def movies_gender_page(request):
    if "search" in request.GET and request.GET.get("q"):
        gender = request.GET.get("q").replace("-", " ").title()

        search_term = request.GET.get("search", "")
        
        movies = Movie.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).filter(
                    gender__name__iexact=gender).exclude(format__format__iexact="3d").order_by("title_eng")
        movies = movies.annotate(
                k1=Case(
                    When(title_eng__istartswith=search_term, then=Value(1.0)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k2=Case(
                    When(title_eng__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k3=Case(
                    When(title__istartswith=search_term, then=Value(1)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                k4=Case(
                    When(title__icontains=search_term, then=Value(0.5)),
                    default=Value(0.0),
                    output_field=FloatField(),
                ),
                rank=F("k1") + F("k2"),
                rank2=F("k3") + F("k4"),
                
            ).exclude(rank=0.0, rank2=0.0).distinct().order_by("-rank", "-rank2", "title_eng")
        print(movies)
        return render(
            request,
            template_name="pages/movies_filter.html",
            context={"movies": movies},
        )
    if not request.GET.get("q"):
        genders = Gender.objects.all().exclude(
            name__in=["Documental", "Fantástico"]
        )
        return render(
            request,
            template_name="pages/movies_gender.html",
            context={"genders": genders},
        )
    else:
        gender = request.GET.get("q").replace("-", " ").title()
        initial = (
            f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
            if request.GET.get("init") != "no"
            else "^[0-9]"
        )
        movies = (
            Movie.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).filter(gender__name__iexact=gender)
                .filter(title_eng__regex=initial)
                .exclude(format__format__iexact="3d").all().order_by("title_eng")
        )
        if request.GET.get("init") == "no":
            movies = movies.annotate(my_integer_field=Cast(Func(F(
                'title_eng'), Value('[^\d]'), Value(''), Value('g'),
                function='regexp_replace'), IntegerField())).order_by(
                "my_integer_field", "title_eng")
            movies = sorted(movies, key=lambda x: int(re.search(r'\d+', x.title_eng.strip()).group()), reverse=False)
        return render(
            request,
            template_name="pages/movies_filter.html",
            context={"movies": movies},
        )

@cache_page(60 * 1440)
def movies_actors_page(request):
    initial = (
        f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
        if request.GET.get("init")
        else "^[aA]"
    )
    actors = Actor.objects.filter(display=True).filter(
        name__regex=initial).all()
    return render(
        request,
        template_name="pages/movies_filter_actors.html",
        context={"actors": actors},
    )

@cache_page(60 * 1440)
def admin_video_list_page(request):
    return render(
        request,
        template_name="admin/video_list.html",
    )

@cache_page(60 * 1440)
def admin_audio_list_page(request):
    return render(
        request,
        template_name="admin/audio_list.html",
    )


class MovieDetail(DetailView):
    model = Movie
    template_name = "pages/movies_details.html"


class SagaDetail(DetailView):
    model = Sagas
    template_name = "pages/saga_details.html"


class ComboDetail(DetailView):
    model = Combo
    template_name = "pages/combo_details.html"


class ActorDetail(DetailView):
    model = Actor
    template_name = "pages/actor_details.html"


class DocumentalDetail(DetailView):
    model = Documental
    template_name = "pages/documental_details.html"


class HumorDetail(DetailView):
    model = Humor
    template_name = "pages/humor_details.html"

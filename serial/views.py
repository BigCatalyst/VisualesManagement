import re
from django.db.models.expressions import Func, F, Value
from django.db.models.fields import IntegerField, FloatField
from django.db.models import Q, Avg, Case, When
from django.db.models.functions import Cast
from django.shortcuts import render
from django.views.generic import DetailView
from movie.models import Actor
from serial.models import Serial
from django.views.decorators.cache import cache_page


@cache_page(60 * 1440)
def series_page(request):
    if request.GET.get("q"):
        initial = (
            f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
            if request.GET.get("init") != "no"
            else "^[0-9]"
        )
        if request.GET.get("q") == "animado" or request.GET.get("q") == "manga":
            series = Serial.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).filter(
                gender__name__iexact=request.GET.get("q")
            ).filter(title_eng__regex=initial).order_by("title_eng")
        elif request.GET.get("q").startswith("gender-"):
            series = Serial.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).filter(
                gender__name__iexact=request.GET.get("q").split("gender-")[-1]
            ).filter(title_eng__regex=initial).order_by("title_eng")
        else:
            series = Serial.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).exclude(
                gender__name__in=["Manga", "Animado"]).filter(type__iexact=request.GET.get("q")).filter(
                title_eng__regex=initial
            ).order_by("title_eng")
        if "search" in request.GET:
            if request.GET.get("q") == "animado" or request.GET.get("q") == "manga":
                series = Serial.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).filter(
                    gender__name__iexact=request.GET.get("q")
                )
            elif request.GET.get("q").startswith("gender-"):
                series = Serial.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).filter(
                    gender__name__iexact=request.GET.get("q").split("gender-")[-1]
                )
            else:
                series = Serial.objects.exclude(Q(origen="Cuba") | Q(origen="CU")).exclude(
                    gender__name__in=["Manga", "Animado"]).filter(type__iexact=request.GET.get("q"))
            search_term = request.GET.get("search", "")
            series = series.annotate(
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
                template_name="pages/series_filter.html",
                context={"movies": series},
            )
        
        if request.GET.get("init") == "no":
            series = series.annotate(my_integer_field=Cast(Func(F(
                'title_eng'), Value('[^\d]'), Value(''), Value('g'),
                function='regexp_replace'), IntegerField())).order_by(
                "my_integer_field", "title_eng")
            series = sorted(series, key=lambda x: int(re.search(r'\d+', x.title_eng.strip()).group()), reverse=False)
            
        return render(
            request,
            template_name="pages/series_filter.html",
            context={"movies": series},
        )

    return render(request, template_name="pages/series.html")

@cache_page(60 * 1440)
def novela_page(request):
    return render(request, template_name="pages/novelas.html")


class SerialDetail(DetailView):
    model = Serial
    template_name = "pages/series_details.html"


class ActorDetail(DetailView):
    model = Actor
    template_name = "pages/actor_series_details.html"

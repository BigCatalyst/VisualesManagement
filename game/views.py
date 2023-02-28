import re
from django.shortcuts import render
from django.db.models.expressions import Func, F, Value
from django.db.models.fields import IntegerField, FloatField
from django.db.models import Q, Avg, Case, When
from django.db.models.functions import Cast
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from game.forms import GameForm
from game.models import Category, Game
from django.views.decorators.cache import cache_page

@cache_page(60 * 1440)
def games_page(request):
    if request.GET.get("q") and request.GET.get("init"):
        initial = (
            f"^[{request.GET.get('init').upper()}{request.GET.get('init').upper()}]"
            if request.GET.get("init") != "no"
            else "^[0-9]"
        )
        if "search" in request.GET:
            search_term = request.GET.get("search", "")
            games = Game.objects.filter(
                category__name__iexact=request.GET.get("q").lower()
                ).annotate(
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
        else:
            if initial == "no":
                
                games = Game.objects.filter(
                    category__name__iexact=request.GET.get("q").lower()
                ).filter(name__regex=initial).annotate(my_integer_field=Cast(Func(F(
                    'name'), Value('[^\d]'), Value(''), Value('g'),
                    function='regexp_replace'), IntegerField())).order_by(
                    "my_integer_field", "name")
                games = sorted(games, key=lambda x: int(re.search(r'\d+', x.name.strip()).group()), reverse=False)
            else:
                games = Game.objects.filter(
                    category__name__iexact=request.GET.get("q").lower()
                ).filter(name__regex=initial)
            
        return render(
            request,
            template_name="pages/games_filter.html",
            context={"movies": games},
        )
    categories = Category.objects.all()
    categories = [
        list(categories)[s : s + 4] for s in range(0, len(categories), 4)  # noqa E203
    ]
    return render(
        request, template_name="pages/games.html", context={"categories": categories}
    )


class GameCreateView(CreateView):
    model = Game
    form_class = GameForm
    template_name = ""
    success_url = reverse_lazy("")


class GameDetail(DetailView):
    model = Game
    template_name = "pages/games_details.html"

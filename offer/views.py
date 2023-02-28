from django.shortcuts import render
from django.views.generic import ListView, DetailView
from game.models import Category, Game
from movie.models import Movie
from music.models import DVD, Author, Collection, Concert, Album
from offer.models import Offer
from serial.models import Serial


def offers_page(request):
    return render(request, template_name="pages/offers.html")


def offers_type_page(request):
    return render(request, template_name="pages/tipo_oferta.html")


def latest_media_page(request):
    movies = (
        Movie.objects.exclude(gender__name__in=["Manga", "Animado"])
        .order_by("-id")
        .values_list("id", flat=True)[:25]
    )
    movies = (
        Movie.objects.filter(id__in=list(movies)).filter(
            title_eng__icontains=request.GET.get("q")
        ).order_by("-id")
        if request.GET.get("q")
        else Movie.objects.filter(id__in=list(movies)).order_by("-id")
    )
    if request.GET.get("filter") and request.GET.get("filter") == "series":
        movies = (
            Serial.objects.exclude(gender__name__in=["Manga", "Animado"])
            .filter(type="Serie")
            .order_by("-id")
            .values_list("id", flat=True)[:25]
        )
        movies = (
            Serial.objects.filter(id__in=list(movies)).filter(
                title_eng__icontains=request.GET.get("q").order_by("-id")
            )
            if request.GET.get("q")
            else Serial.objects.filter(id__in=list(movies)).order_by("-id")
        )
    elif request.GET.get("filter") and request.GET.get("filter") == "miniseries":
        movies = (
            Serial.objects.exclude(gender__name__in=["Manga", "Animado"])
            .filter(type="Miniserie")
            .order_by("-id")
            .values_list("id", flat=True)[:25]
        )
        movies = (
            Serial.objects.filter(id__in=list(movies)).filter(
                title_eng__icontains=request.GET.get("q")
            ).order_by("-id")
            if request.GET.get("q")
            else Serial.objects.filter(id__in=list(movies)).order_by("-id")
        )
    elif request.GET.get("filter") and request.GET.get("filter") == "doramas":
        movies = (
            Serial.objects.filter(type="Dorama")
            .order_by("-id")
            .values_list("id", flat=True)[:25]
        )
        movies = (
            Serial.objects.filter(id__in=list(movies)).filter(
                title_eng__icontains=request.GET.get("q")
            ).order_by("-id")
            if request.GET.get("q")
            else Serial.objects.filter(id__in=list(movies)).order_by("-id")
        )
    elif request.GET.get("filter") and request.GET.get("filter") == "novelas":
        movies = (
            Serial.objects.filter(type="Novela")
            .order_by("-id")
            .values_list("id", flat=True)[:25]
        )
        movies = (
            Serial.objects.filter(id__in=list(movies)).filter(
                title_eng__icontains=request.GET.get("q")
            ).order_by("-id")
            if request.GET.get("q")
            else Serial.objects.filter(id__in=list(movies)).order_by("-id")
        )
    elif request.GET.get("filter") and request.GET.get("filter") == "series-animadas":
        movies = (
            Serial.objects.filter(gender__name="Animado")
            .order_by("-id")
            .values_list("id", flat=True)[:25]
        )
        movies = (
            Serial.objects.filter(id__in=list(movies)).filter(
                title_eng__icontains=request.GET.get("q")
            ).order_by("-id")
            if request.GET.get("q")
            else Serial.objects.filter(id__in=list(movies)).order_by("-id")
        )
    elif request.GET.get("filter") and request.GET.get("filter") == "series-mangas":
        movies = (
            Serial.objects.filter(gender__name="Manga")
            .order_by("-id")
            .values_list("id", flat=True)[:25]
        )
        movies = (
            Serial.objects.filter(id__in=list(movies)).filter(
                title_eng__icontains=request.GET.get("q")
            ).order_by("-id")
            if request.GET.get("q")
            else Serial.objects.filter(id__in=list(movies)).order_by("-id")
        )
    elif (
        request.GET.get("filter") and request.GET.get("filter") == "películas-animadas"
    ):
        movies = (
            Movie.objects.filter(gender__name="Animado")
            .order_by("-id")
            .values_list("id", flat=True)[:25]
        )
        movies = (
            Movie.objects.filter(id__in=list(movies)).filter(
                title_eng__icontains=request.GET.get("q")
            ).order_by("-id")
            if request.GET.get("q")
            else Movie.objects.filter(id__in=list(movies)).order_by("-id")
        )
    elif request.GET.get("filter") and request.GET.get("filter") == "películas-mangas":
        list_id = (
            Movie.objects.filter(gender__name="Manga")
            .order_by("-id")
            .values_list("id", flat=True)[:25]
        )
        movies = (
            Movie.objects.filter(id__in=list(list_id)).filter(
                title_eng__icontains=request.GET.get("q")
            ).order_by("-id")
            if request.GET.get("q")
            else Movie.objects.filter(id__in=list(list_id)).order_by("-id")
        )
    elif request.GET.get("filter") and request.GET.get("filter") == "colecciones":
        list_id = (
            Collection.objects.all().order_by("-id").values_list("id", flat=True)[:25]
        )
        movies = (
            Collection.objects.filter(id__in=list(list_id)).filter(
                name__icontains=request.GET.get("q")
            ).order_by("-id")
            if request.GET.get("q")
            else Collection.objects.filter(id__in=list(list_id)).order_by("-id")
        )
    elif request.GET.get("filter") and request.GET.get("filter") == "dvd":
        list_id = DVD.objects.all().order_by("-id").values_list("id", flat=True)[:25]
        movies = (
            DVD.objects.filter(id__in=list(list_id)).filter(
                title__icontains=request.GET.get("q")
            ).order_by("-id")
            if request.GET.get("q")
            else DVD.objects.filter(id__in=list(list_id)).order_by("-id")
        )
    elif request.GET.get("filter") and request.GET.get("filter") == "discografía":
        list_id = Album.objects.all().order_by("-id")[:25]
        movies = (
            Author.objects.filter(
                title__icontains=request.GET.get("q")
            ).distinct().order_by("-id")[:25]
            if request.GET.get("q")
            else Author.objects.distinct().order_by("-id")[:25]
        )
    elif request.GET.get("filter") and request.GET.get("filter") == "conciertos":
        list_id = Concert.objects.all().order_by("-id").values_list("id", flat=True)[:25]
        movies = (
            Concert.objects.filter(id__in=list(list_id)).filter(
                name__icontains=request.GET.get("q")
            ).order_by("-id")
            if request.GET.get("q")
            else Concert.objects.filter(id__in=list(list_id)).order_by("-id")
        )
    elif request.GET.get("filter") and request.GET.get("filter") != "películas":
        list_id = (
            Game.objects.filter(
                category__name__iexact=request.GET.get("filter").lower()
            )
            .order_by("-id")
            .values_list("id", flat=True)[:25]
        )
        movies = (
            Game.objects.filter(id__in=list(list_id)).filter(
                name__icontains=request.GET.get("q")
            ).order_by("-id")
            if request.GET.get("q")
            else Game.objects.filter(id__in=list(list_id)).order_by("-id")
        )

    return render(
        request,
        template_name="pages/new.html",
        context={"categories": Category.objects.all(), "movies": movies[:25]},
    )


class OfferList(ListView):
    model = Offer
    template_name = "pages/offers_list.html"

    def get_queryset(self):
        if self.request.GET.get("q"):
            return Offer.objects.filter(type=self.request.GET.get("q")).order_by("name")
            
class OfferDetail(DetailView):
    model = Offer
    template_name = "pages/offers_details.html"


import json
import os
import sys
from pathlib import Path

import tempfile
from django.shortcuts import render
import imdb
import requests
import urllib.request
import urllib3
from bs4 import BeautifulSoup
from django.core.files import File
from django.db.utils import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.timezone import now
from django.views.generic import CreateView
from googletrans import Translator
from imdb import Movie as ImdbMovie
from python_filmaffinity import FilmAffinity
from tqdm.asyncio import tqdm

from actor.models import Actor
from cinema import rawgpy
from game.models import Game
from game.models import GameCapture
from movie.models import Movie, Gender, Sagas, Combo, Documental, \
    DocumentalSeason, Sport, Format
from music.models import Author, Album, Collection, Concert, DVD, Song
from serial.models import Serial, Season
from offer.models import Offer
from tasks.license import activate_license
from tasks.models import License
from collections import defaultdict

from movie.admin import MovieResource, ActorResource
from serial.admin import SerialResource
from django.core.files.storage import FileSystemStorage

translator = Translator()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
rawg = rawgpy.RAWG("User-Agent, CINEMA")

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
APPS_DIR = str(ROOT_DIR / "cinema")


class LicenseView(CreateView):
    model = License
    template_name = "license.html"
    success_url = reverse_lazy("home")
    fields = ["license_id", "key"]

    def form_valid(self, form):
        activated, msg = activate_license(form.instance.license_id,
                                          form.instance.key)
        if not activated:
            print(msg)
            form.errors["error"] = msg
            return render(self.request, self.template_name,
                          context={"form": form})
        return HttpResponseRedirect(self.success_url)


def download_file_from_url(url, name):
    # Stream the image from the url
    try:
        request = requests.get(url, stream=True)
    except requests.exceptions.RequestException as e:
        # TODO: log error here
        return None

    if request.status_code != requests.codes.ok:
        # TODO: log error here
        return None

    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()

    # Read the streamed image in sections
    for block in request.iter_content(1024 * 8):

        # If no more file then stop
        if not block:
            break

        # Write image block to temporary file
        lf.write(block)

    return File(lf, name=name + ".jpg")


def url_clean(url):
    base, ext = os.path.splitext(url)
    i = url.count('@')
    s2 = url.split('@')[0]
    url = s2 + '@' * i + ext
    return url


def _filter_movie_imdb(movies: list, year: int = None, country: str = None,
                       kind: str = 'movie') -> ImdbMovie or None:
    ia = imdb.IMDb()
    for m in filter(lambda x: x.data["kind"] == kind and (
        "year" in x.data and x.data["year"] == int(year)), movies):
        movie = ia.get_movie(m.movieID)
        if year and ("year" in movie.data and movie.data["year"] == int(year)):
            if country and (
                "countries" in movie.data and country in movie.data["countries"]
            ):
                return movie
            elif not country:
                return movie
        else:
            if country and (
                "countries" in movie.data and country in movie.data["countries"]
            ):
                return movie
    return None


def _filter_movie_filmaffinity(movies: list, year: int = None,
                               country: str = None, kind: str = 'movie'):
    ia = FilmAffinity(lang="en")
    filtered = filter(
        lambda x: (x["title"].lower().find(kind.split(" ")[0]) > -1 and x[
            "title"].lower().find(kind.split(" ")[1]) > -1), movies) if (
        kind != 'movie') else movies
    if len(list(filtered)) == 1 and int(year) - 1 <= int(
        filtered[0]["year"]) <= int(year) + 1:
        return filtered[0]

    for m in filtered:
        movie = ia.get_movie(id=m["id"])
        if year and (
            "year" in movie and int(year) - 1 <= int(movie["year"]) >= int(
            year) + 1
        ):
            if country and (
                "country" in movie and country in movie["country"]
            ):
                return movie
            elif not country:
                return movie
        else:
            if country and (
                "country" in movie and country in movie["country"]
            ):
                return movie
    return None


def movies_imdb():
    ia = imdb.IMDb()
    filtered = Movie.objects.filter(imdb=False).filter(
        Q(synopsis=None) | Q(synopsis='') | Q(duration=None)
    ).all()
    local_movies = filtered[:len(filtered) // 10 + 1] if len(filtered) >= 1000 else filtered[:100]
    movies_id = local_movies.values_list("id", flat=True)
    for m in tqdm(local_movies):
        movies = ia.search_movie(m.title_eng.strip().rstrip(), results="100")
        country = translator.translate(
            m.origen + " país", src="es", dest="en").text.split(" ")[0] if (
            m.origen and len(m.origen.split(" ")) == 1) else (
            translator.translate(m.origen, src="es", dest="en").text)
        movie = _filter_movie_imdb(
            movies, m.year, country)
        if not movie and m.year:
            movie = _filter_movie_imdb(
                movies, m.year - 1, country)
            if not movie:
                movie = _filter_movie_imdb(
                    movies, m.year + 1, country)

        if movie:
            plot = None
            if "plot" in movie.data:
                for p in movie.data["plot"]:
                    if len(p) < 500:
                        plot = p
            elif plot is None and "synopsis" in movie.data:
                for p in movie.data["synopsis"]:
                    if len(p) < 500:
                        plot = p
            if plot:
                translation = translator.translate(plot, src="en", dest="es")
                m.synopsis = translation.text
            if not m.year or m.year != movie.data["year"]:
                m.year = movie.data["year"]
            if not m.duration:
                m.duration = "%02d.%02d" % (
                    divmod(int(movie["runtime"][0]), 60))
            if not m.photo:
                photo = download_file_from_url(
                    url_clean(movie.data["cover url"]), m.title_eng)
                if photo:    
                    fs = FileSystemStorage(location="cinema/media/peliculas/descargas/")
                    path = "peliculas/descargas/" + m.title_eng + ".jpg"
                    filename = fs.save( m.title_eng + ".jpg", photo)
                    m.photo = path
            m.gender = Gender.objects.filter(name=translator.translate(
                movie.data["genres"][0], src="en", dest="es").text).first()
            m.sub_gender = ", ".join(
                [translator.translate(genre, src="en", dest="es").text
                 for genre in movie.data["genres"]])
            actors = []
            for actor in movie.data["cast"]:
                person = ia.get_person(actor.personID)
                try:
                    _actor, created = Actor.objects.get_or_create(name=person[
                        "name"])
                    if created:
                        photo = download_file_from_url(
                            url_clean(person['headshot']),
                            _actor.name) if "headshot" in person else None
                        if photo:    
                            fs = FileSystemStorage(location="cinema/media/actores/descargas/")
                            path = "actores/descargas/" + _actor.name + ".jpg"
                            filename = fs.save( _actor.name + ".jpg", photo)
                            _actor.photo = path
                            _actor.save()
                    actors.append(_actor.id)
                except KeyError:
                    pass
            m.save()
            m.actor.set(actors)
        m.imdb = True
        m.save()
    
	

def actors_imdb():
    ia = imdb.IMDb()
    actors = Actor.objects.filter(imdb=False,
                                  photo='').all()
    actors = actors[:len(actors) // 10 + 1] if len(actors) >= 1000 else actors[:100]

    for actor in actors:
        name = actor.name.strip().rstrip()
        persons = ia.search_person(name)
        persons = list(filter(lambda x: x["name"] == name, persons))
        if persons:
            person = ia.get_person(persons[0].personID)
            photo = download_file_from_url(
                url_clean(person['headshot']),
                actor.name) if "headshot" in person else None
            if photo:
                fs = FileSystemStorage(location="cinema/media/actores/descargas/")
                path = "actores/descargas/" + actor.name + ".jpg"
                filename = fs.save( actor.name + ".jpg", photo)
                actor.photo = path
        actor.imdb = True
        actor.save()
	


def series_imdb():
    ia = imdb.IMDb()
    filtered = Serial.objects.filter(imdb=False).filter(
        Q(synopsis=None) | Q(synopsis='')
    ).all()
    local_movies = filtered[:len(filtered) // 10 + 1] if len(filtered) >= 1000 else filtered[:100]
    series_id = local_movies.values_list("id", flat=True)
    for m in tqdm(local_movies):
        movies = ia.search_movie(m.title_eng.strip().rstrip(), results="100")
        country = translator.translate(
            m.origen + " país", src="es", dest="en").text.split(" ")[0] if (
            m.origen and len(m.origen.split(" ")) == 1) else (
            translator.translate(m.origen, src="es", dest="en").text)
        if len(movies) == 1 and movies[0]['kind'] == 'tv series' and movies[0][
            "year"] == int(m.season_set.all()[0].year):
            movie = ia.get_movie(movies[0].movieID)
        else:
            movie = _filter_movie_imdb(
                movies, m.season_set.all()[0].year,
                country, kind='tv series')
        if not movie and m.season_set.all()[0].year:
            movie = _filter_movie_imdb(movies, m.season_set.all()[0].year - 1,
                                       country)
            if not movie:
                movie = _filter_movie_imdb(movies,
                                           m.season_set.all()[0].year + 1,
                                           country)

        if movie:
            plot = None
            if "plot" in movie.data:
                for p in movie.data["plot"]:
                    if len(p) < 500:
                        plot = p
            elif plot is None and "synopsis" in movie.data:
                for p in movie.data["synopsis"]:
                    if len(p) < 500:
                        plot = p
            if plot:
                translation = translator.translate(plot, src="en", dest="es")
                m.synopsis = translation.text
            if not m.photo:
                photo = download_file_from_url(
                    url_clean(movie.data["cover url"]), m.title_eng)
                if photo:    
                    fs = FileSystemStorage(location="cinema/media/series/descargas/")
                    path = "series/descargas/" + m.title_eng + ".jpg"
                    filename = fs.save( m.title_eng + ".jpg", photo)
                    m.photo = path
            m.gender = Gender.objects.filter(name=translator.translate(
                movie.data["genres"][0], src="en", dest="es").text).first()
            actors = []
            for actor in movie.data["cast"]:
                person = ia.get_person(actor.personID)
                try:
                    _actor, created = Actor.objects.get_or_create(name=person[
                        "name"])
                    if created:
                        photo = download_file_from_url(
                            url_clean(person['headshot']),
                            _actor.name) if "headshot" in person else None
                        if photo:    
                            fs = FileSystemStorage(location="cinema/media/actores/descargas/")
                            path = "actores/descargas/" + _actor.name + ".jpg"
                            filename = fs.save( _actor.name + ".jpg", photo)
                            _actor.photo = path
                            _actor.save()
                    actors.append(_actor.id)
                    
                except KeyError:
                    pass
            m.save()
            m.actor.set(actors)
        m.imdb = True
        m.save()
	
    queryset = Serial.objects.filter(id__in=series_id)
    resource = SerialResource()
    dataset = resource.export(queryset=queryset)
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}_{}.xlsx"'.format(
                str(_("Series")), str(int(''.join(c for c in str(now().today().date()) if c.isdigit()))))
    return response


def movies_filmaffinity():
    filtered = Movie.objects.filter(film_affinity=False).filter(
        Q(synopsis=None) |
        Q(duration=None)
    ).all()
    local_movies = filtered[:len(filtered) // 10 + 1] if len(filtered) >= 1000 else filtered[:100]
    for m in tqdm(local_movies):
        ia = FilmAffinity(lang="en")
        movies = ia.search(title=m.title_eng.strip().rstrip(), top=100,
                           from_year=m.year if m.year else 1900,
                           to_year=m.year if m.year else now().year
                           )
        country = translator.translate(
            m.origen + " país", src="es", dest="en").text.split(" ")[0] if (
            m.origen and len(m.origen.split(" ")) == 1) else (
            translator.translate(m.origen, src="es", dest="en").text)
        movie = _filter_movie_filmaffinity(movies, m.year,
                                           country)
        if not movie and m.actor.all().exists():
            ia = FilmAffinity()
            movies = ia.search(title=m.title_eng.strip().rstrip(), top=100,
                               from_year=m.year - 1 if m.year else 1900,
                               to_year=m.year + 1 if m.year else now().year,
                               cast=m.actor.all()[0].name
                               )
            movie = _filter_movie_filmaffinity(
                movies, m.year, country)

        if movie:
            ia = FilmAffinity()
            movie = ia.get_movie(id=movie["id"], images=True)
            plot = None
            if "description" in movie:
                for p in movie["description"]:
                    if len(p) < 500:
                        plot = p
            if plot:
                m.synopsis = plot
            if not m.year or (movie["year"] and m.year != int(movie["year"])):
                m.year = int(movie["year"])
            if not m.duration:
                m.duration = "%02d.%02d" % (
                    divmod(int(movie["duration"].split(" ")[0]), 60))
            if not m.photo:
                m.photo = download_file_from_url(
                    movie["images"]["posters"][0]["image"], m.title_eng)
            m.gender = Gender.objects.filter(name__icontains=movie["genre"][
                0]).first()
            m.sub_gender = ", ".join(
                [translator.translate(genre, src="en", dest="es").text
                 for genre in movie["genre"]])
            actors = []
            ia = imdb.IMDb()
            for actor in movie["actors"]:
                name = actor.strip().rstrip()
                persons = ia.search_person(name)
                persons = list(filter(lambda x: x["name"] == name, persons))
                if persons:
                    person = ia.get_person(persons[0].personID)
                    try:
                        _actor, created = Actor.objects.get_or_create(
                            name=person[
                                "name"])
                        if created:
                            _actor.photo = download_file_from_url(
                                url_clean(person['headshot']),
                                _actor.name) if "headshot" in person else None
                            _actor.save()
                        actors.append(_actor.id)
                    except KeyError:
                        pass
            m.save()
            m.actor.set(actors)
        m.film_affinity = True
        m.save()


def get_games():
    filtered = Game.objects.filter(rawg=False).filter(
        Q(synopsis=None) | Q(synopsis='') | Q(captures=None)
    ).all()
    return filtered[:len(filtered) // 10 + 1] if len(filtered) >= 1000 else filtered[:100]


def games_rawg_io():

    for game in get_games():
        games_list = rawg.search(game.name)

        rawg_game = list(filter(
            lambda
                r: r.name.lower() == game.name.lower() or game.name.lower().find(
                r.name.lower()) != -1, games_list))
        
        if rawg_game:
            rawg_game = rawg.get_game(rawg_game[0].slug)
            if rawg_game.description_raw is not None or rawg_game.description_raw != '':
                synopsis = rawg_game.description_raw if 0 < len(rawg_game.description_raw) < 500 else None
                if synopsis:
                    game.synopsis = translator.translate(synopsis, dest="es", src="en").text
            
            if not game.captures.all().exists():
                images = rawg.game_screenshots(game_pk=str(rawg_game.slug))
                for i, img in enumerate(images[:3]):
                    photo = download_file_from_url(img, game.name+"_"+str(i))
                    if photo:
                        fs = FileSystemStorage(location="cinema/media/juegos/capturas/descargas/")
                        path = "juegos/capturas/descargas/" + game.name+"_"+str(i) + ".jpg"
                        filename = fs.save( game.name+"_"+str(i) + ".jpg", photo)
                        capture = GameCapture()
                        capture.game = game
                        capture.image = path
                        capture.save()
            if not game.photo or game.photo == '':
                game_image = rawg_game.background_image
                photo = download_file_from_url(game_image, game.name+"_"+str(i))
                if photo:
                    fs = FileSystemStorage(location="cinema/media/juegos/descargas/")
                    path = "juegos/descargas/" + game.name+"_"+str(i) + ".jpg"
                    filename = fs.save( game.name+"_"+str(i) + ".jpg", photo)
                    game.photo = path
        game.rawg = True
        game.save()


def author_coveralia():
    authors = Author.objects.filter(
        Q(photo=None) | Q(photo='')
    ).values_list("name", flat=True)
    url = "https://www.coveralia.com/galeriadefotos/{}.php"
    img_url = "https://images.coveralia.com/autores/fotos/{}.jpg"
    for author in authors:
        page = urllib.request.Request(url.format(author.lower().replace(" ", "-")))
        result = urllib.request.urlopen(page)     
        resulttext = result.read()
        soup = BeautifulSoup(resulttext, 'html.parser')
        soup = soup.find_all(class_= "lista_normal margen5")[0]
        links = [a['href'] for a in soup.find_all('a', href=True)]
        links = [*dict.fromkeys(links)]

        img_id = links[2].split("/")[-1].split(".php")[0]
        path = APPS_DIR + 'Temp/autores/{}'.format(author)
        isExist = os.path.exists(path)

        if not isExist:
            os.makedirs(path, exist_ok=False)
        img_path = path+"/{}.jpg".format(img_id)
        with open(img_path, 'wb') as f:
            f.write(requests.get(img_url.format(img_id)).content)
            f.close()

def album_coveralia():
    albums = Album.objects.filter(
        Q(photo=None) | Q(photo='') | Q(photo_back=None) | Q(photo_back='')
    ).all()
    url = "https://www.coveralia.com/caratulas-de/{}.php"
    img_url_frontal = "https://images.coveralia.com/audio/{init}/{album}-Frontal.jpg"
    img_url_back = "https://images.coveralia.com/audio/{init}/{album}-Trasera.jpg"
    for album in albums:
        author = album.author.name
        page = urllib.request.Request(url.format(author.lower().replace(" ", "-")))
        result = urllib.request.urlopen(page)     
        resulttext = result.read()
        soup = BeautifulSoup(resulttext, 'html.parser')
        soup = soup.find_all(class_= "caja_azul margen5")
        for soup1 in soup:
            for a, span in zip(soup1.find_all("a"), soup1.find_all("span")):
                if album.title in a.text and str(album.year) in span.text:
                    _soup = soup1.find_all(class_= "lista_normal izquierda")[0]
                    for a_tag in _soup.find_all("a"):
                        if a_tag.text == "Frontal":
                            img_id = a["href"].split("/")[-1].split(".php")[0]
                            path = 'albums/{}/{}'.format(author,album.title)
                            isExist = os.path.exists(path)
                            if not isExist:
                                os.makedirs(path, exist_ok=False)
                            img_path = path+"/{}-Frontal.jpg".format(img_id)
                            with open(img_path, 'wb') as f:
                                rq = requests.get(img_url_frontal.format(init=author[0].lower(), album=img_id))
                                if rq.status_code == 200:
                                    f.write(rq.content)
                                else:
                                    rq = requests.get(img_url_frontal.format(init=author[0].lower(), album=img_id.capitalize()))
                                    if rq.status_code == 200:
                                        f.write(rq.content)
                                    else:
                                        rq = requests.get(img_url_frontal.format(init=author[0].lower(), album=img_id.title()))
                                        f.write(rq.content)
                                f.close()
                        if a_tag.text == "Trasera":
                            img_id = a["href"].split("/")[-1].split(".php")[0]
                            path = 'albums/{}/{}'.format(author,album.title)
                            isExist = os.path.exists(path)
                            if not isExist:
                                os.makedirs(path, exist_ok=False)
                            img_path = path+"/{}-Trasera.jpg".format(img_id)
                            with open(img_path, 'wb') as f:
                                rq = requests.get(img_url_back.format(init=author[0].lower(), album=img_id))
                                if rq.status_code == 200:
                                    f.write(rq.content)
                                else:
                                    rq = requests.get(img_url_back.format(init=author[0].lower(), album=img_id.capitalize()))
                                    if rq.status_code == 200:
                                        f.write(rq.content)
                                    else:
                                        rq = requests.get(img_url_back.format(init=author[0].lower(), album=img_id.title()))
                                        f.write(rq.content)
                                f.close()            

def review_empty_fields():
    for movie in Movie.objects.filter(
        Q(synopsis=None) | Q(synopsis='') | Q(duration=None)
    ).all():
        movie.imdb = False
        movie.film_affinity = False
        movie.save()

    for s in Serial.objects.filter(
        Q(synopsis=None) | Q(synopsis='')
    ).all():
        s.imdb = False
        s.film_affinity = False
        s.save()

    for game in Game.objects.filter(
        Q(synopsis=None) | Q(synopsis='') | Q(captures=None)
    ).all():
        game.rawg = False
        game.save()


def upload_actor():
    # Opening JSON file
    f = open('data/actor.json', encoding='utf-8')
    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    for i in data:
        if i["Nombre"] is not None or i["Nombre"] != '':
            actor, created = Actor.objects.get_or_create(
                id=i["Id"],
                defaults={"name": i["Nombre"]})
            if i["FotoActor"] != "":
                actor.photo = "actores/" + i["FotoActor"]
                actor.save()
    # Closing file
    f.close()


def upload_movie():
    # Opening JSON file
    with open('data/movies.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data:
            saga = None
            if i["Saga"] != "":
                saga, saga_created = Sagas.objects.get_or_create(
                    title=i["Saga"])
            if i["NombreIng"] is not None or i["NombreIng"] != '':
                movie, created = Movie.objects.update_or_create(
                    id=i["Id"],
                    defaults={
                        "title_eng": i["NombreIng"],
                        "title": i["Nombre"],
                        "gender_id": i["Genero"] if i["Genero"] != "" else "Acción",
                        "sub_gender": i["Subgenero"],
                        "duration": i["Duracion"],
                        "year": i["Anno"],
                        "origen": i["Origen"],
                        "format_id": i["Formato"] if i["Formato"] != "" else "No",
                        "synopsis": i["Sinopsis"],
                        "saga": saga if saga else None,
                        "definition": i["Definicion"].upper(),
                        "language": i["Idioma"],
                    })
                if i["FotoPelicula"] != "":
                    movie.photo = "peliculas/" + i["FotoPelicula"]
                    movie.save()
        # Closing file
        f.close()

def update_movie_definition():
    # Opening JSON file
    with open('data/movies.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        up_movies = []
        for i in data:
            if i["NombreIng"] is not None or i["NombreIng"] != '':
                movie = Movie.objects.filter(
                    id=i["Id"])
                if not movie.exists():
                    print(i["Id"])
                    up_movies.append(i["Id"])
                else:
                    movie = movie.first()
                    movie.definition = i["Definicion"].upper().strip().rstrip().replace(" ", "")
                    movie.save()
        # Closing file
        f.close()


def upload_actor_movie():
    # Opening JSON file
    with open('data/actorpeliculas.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        dct = {}
        for i in data:
            if i["PeliculaId"] in dct and i["ActorId"] not in dct[i["PeliculaId"]]:
                actor = Actor.objects.get(id=i["ActorId"])
                film = i["PeliculaId"]
                dct[film].append(actor)
            elif i["PeliculaId"] not in dct:
                dct[i["PeliculaId"]] = []
            elif i["PeliculaId"] in dct and i["ActorId"] in dct[i["PeliculaId"]]:
                pass
        print(dct["11117"])
        for movie in Movie.objects.all():
            movie.actor.set(dct[movie.id])
        
        # Closing file
        f.close()


def upload_actor_series():
    # Opening JSON file
    f = open('data/actorseries.json', encoding='utf-8')
    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    dct = defaultdict(list)
    for i in data:
        if i["SerieId"] in dct and i["ActorId"] not in dct[i["SerieId"]]:
            dct[i["SerieId"]].append(Actor.objects.get(id=i["ActorId"]))
        elif i["SerieId"] not in dct:
            dct[i["SerieId"]].append(Actor.objects.get(id=i["ActorId"]))
    for movie in Serial.objects.all():
        movie.actor.set(dct[movie.id])
        
    f.close()


def upload_series():
    # Opening JSON file
    with open('data/series.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data:
            if i["TituloIng"] is not None or i["TituloIng"] != '':
                in_trans = None
                if "EnCurso" in i:
                    in_trans = i["EnCurso"]
                serial, created = Serial.objects.update_or_create(
                    id=i["Id"],
                    defaults={
                        "title_eng": i["TituloIng"],
                        "title": i["Titulo"],
                        "gender_id": i["Genero"] if i["Genero"] != "" else "Sin Categoria",
                        "type": i["Tipo"],
                        "origen": i["Origen"],
                        "synopsis": i["Sinopsis"],
                        "in_transmission": True if in_trans == "1" else False 
                    })
                if i["FotoSerie"] != "":
                    serial.photo = "series/" + i["FotoSerie"]
                    serial.save()
        # Closing file
        f.close()


def upload_series_seasons():
    # Opening JSON file
    f = open('data/seriestemporadas.json', encoding='utf-8')
    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    for i in data:
        series_temp, created = Season.objects.update_or_create(
            id=i["Id"],
            defaults={
                "chapters": i["Capitulos"],
                "number": i["Temporada"],
                "series_id": i["IdSerie"],
                "year": i["Anno"],
                "format_id": i["Formato"] if i["Formato"] != "" and (
                    Format.objects.filter(format=i["Formato"]).exists()) else "No",
                "language": i["Idioma"],
                "definition": i["Definicion"] if i["Definicion"] != "" else "No"
            }
        )
    # Closing file
    f.close()


def upload_author():
    # Opening JSON file
    f = open('data/author.json', encoding='utf-8')
    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    for i in data:
        if i["Nombre"] is not None or i["Nombre"] != '':
            try:
                author, created = Author.objects.get_or_create(
                    name=i["Nombre"],
                    defaults={"name": i["Nombre"]})
            except IntegrityError:
                author = Author.objects.get(name=i["Nombre"])
            if i["Foto"] != "":
                author.photo = "discografia/" + i["Foto"]
                author.save()
    # Closing file
    f.close()


def upload_albums():
    # Opening JSON file
    with open('data/albums.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data:
            album = None
            _author = Author.objects.filter(id=i["IdAutor"])
            if not _author.exists():
                print(i["Titulo"], i["IdAutor"])
            album, created = Album.objects.update_or_create(
                        id=i["Id"],
                        defaults={
                            "title": i["Titulo"],
                            "year": i["Anno"],
                            "author_id": _author.first().id
                        })
            if album is not None:
                if i["Foto"] != "":
                    album.photo = "album/" + i["Foto"]
                    album.save()
                if i["FotoBack"] != "":
                    album.photo_back = "album/" + i["FotoBack"]
                    album.save()

        # Closing file
        f.close()


def upload_collection():
    # Opening JSON file
    with open('data/collection.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data:
            if i["Nombre"] is not None or i["Nombre"] != '':
                album, created = Collection.objects.update_or_create(
                    id=i["Id"],
                    defaults={
                        "name": i["Nombre"],
                        "gender_id": i["Genero"] if i["Genero"] != "" else "Sin definir",
                        "format_id": i["Formato"] if i["Formato"] != "" else
                        "No"
                    })
                if i["Foto"] != "":
                    album.photo = "coleccion/" + i["Foto"]
                    album.save()
        # Closing file
        f.close()
        
def upload_songs_collection():
    # Opening JSON file
    with open('data/cancioncoleccion.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data:
            if i["TituloCancion"] is not None or i["TituloCancion"] != '':
                album, created = Song.objects.update_or_create(
                    id=i["Id"],
                    defaults={
                        "title": i["TituloCancion"],
                        "success": True if i["Exito"] != "No" else False,
                        "video":  True if i["Video"] != "No" else False,
                        "collection_id": i["IdColeccion"],
                    })
        # Closing file
        f.close()


def upload_combos():
    # Opening JSON file
    with open('data/combos.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data:
            if i["Combo"] is not None or i["Combo"] != '':
                combo, created = Combo.objects.update_or_create(
                    id=i["Id"],
                    defaults={
                        "name": i["Combo"]
                    })
                if i["FotoCombo"] != "":
                    combo.photo = "combos/" + i["FotoCombo"]
                    combo.save()
        # Closing file
        f.close()


def upload_concerts():
    # Opening JSON file
    with open('data/concerts.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data:
            if i["Interprete"] is not None or i["Interprete"] != '':
                combo, created = Concert.objects.update_or_create(
                    id=i["Id"],
                    defaults={
                        "interpreter": i["Interprete"],
                        "year": i["Anno"],
                        "place": i["Lugar"],
                        "definition": i["Definicion"] if i["Definicion"] != "" else "No",
                    })
                if i["Foto"] != "":
                    combo.photo = "concierto/" + i["Foto"]
                    combo.save()
        # Closing file
        f.close()


def upload_documental():
    # Opening JSON file
    with open('data/documental.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data:
            if i["NombreIng"] is not None or i["NombreIng"] != '':
                movie, created = Documental.objects.update_or_create(
                    id=i["Id"],
                    defaults={
                        "title_eng": i["NombreIng"],
                        "title": i["Nombre"],
                        "gender_id": i["Genero"] if i["Genero"] != "" else 21,
                        "duration": i["Duracion"],
                        "year": i["Anno"],
                        "origen": i["Origen"],
                        "format": Format.objects.filter(format=i["Formato"]).first() if Format.objects.filter(format=i["Formato"]).exists() else Format.objects.filter(format="No").first(),
                        "synopsis": i["Sinopsis"],
                        "type": i["TipoDocumental"],
                        "definition": i["Definicion"],
                        "language": i["Idioma"],
                    })
                if i["FotoDocumental"] != "":
                    movie.photo = "documental/" + i["FotoDocumental"]
                    movie.save()
        # Closing file
        f.close()


def upload_documental_seasons():
    # Opening JSON file
    f = open('data/documentaltemporadas.json', encoding='utf-8')
    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    for i in data:
        try:
            documental = Documental.objects.get(id=i["IdDocumental"])
        except Documental.DoesNotExist:
            documental = None
        series_temp, created = DocumentalSeason.objects.update_or_create(
            id=i["Id"],
            defaults={
                "chapters": i["Capitulos"],
                "season": i["Temporada"],
                "documental": documental,
                "year": i["Anno"]
            }
        )
    # Closing file
    f.close()


def upload_dvds():
    # Opening JSON file
    with open('data/dvds.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data:
            if i["Titulo"] is not None or i["Titulo"] != '':
                try:
                    author, author_created = Author.objects.get_or_create(
                        name=i["Autor"])
                    album, created = DVD.objects.update_or_create(
                        id=i["Id"],
                        defaults={
                            "title": i["Titulo"],
                            "year": i["Anno"],
                            "author": author
                        })
                except IntegrityError:
                    print(i["Id"])
                    album = DVD.objects.get(id=i["Id"])
                if i["Foto"] != "":
                    album.photo = "dvd/" + i["Foto"]
                    album.save()
                if i["FotoBack"] != "":
                    album.photo_back = "dvd/" + i["FotoBack"]
                    album.save()
        # Closing file
        f.close()


def upload_games():
    # Opening JSON file
    with open('data/games.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data:
            if i["Nombre"] is not None or i["Nombre"] != '':
                album, created = Game.objects.update_or_create(
                    id=i["Id"],
                    defaults={
                        "name": i["Nombre"],
                        "year": i["Anno"],
                        "category_id": i["IdCategoria"],
                        "synopsis": i["Sinopsis"],
                        "type": i["Tipo"],
                        "size": i["Tamano"],
                        "requirement": i["Requisitos"],
                    })
                if i["Foto"] != "":
                    album.photo = "juegos/" + i["Foto"]
                    album.save()
                if i["Manual"] != "":
                    album.manual = "juegos/manual/" + i["Manual"]
                    album.save()
                GameCapture.objects.filter(game=album).delete()
                for capture in i["Capturas"].split(";"):
                    game_capture = GameCapture()
                    game_capture.game = album
                    game_capture.image = "juegos/capturas/" + capture
                    game_capture.save()
        # Closing file
        f.close()


def upload_sports():
    # Opening JSON file
    with open('data/sports.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data:
            if i["Nombre"] is not None or i["Nombre"] != '':
                album, created = Sport.objects.update_or_create(
                    id=i["Id"],
                    defaults={
                        "name": i["Nombre"],
                        "year": i["Año"],
                        "definition": i["Definicion"] if i["Definicion"] != "" else "No",
                        "format_id": i["Formato"] if i["Formato"] != "" else
                        "No"
                    })
                if i["Foto"] != "":
                    album.photo = "deporte/" + i["Foto"]
                    album.save()

        # Closing file
        f.close()
        
def upload_offers():
    # Opening JSON file
    with open('data/offers.json', encoding='utf-8') as f:
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list
        for i in data:
            if i["Oferta"] is not None or i["Oferta"] != '':
                album, created = Offer.objects.update_or_create(
                    id=i["Id"],
                    defaults={
                        "name": i["Oferta"],
                        "price": i["Precio"],
                        "especial": i["Especial"],
                        "description": i["Descripcion"],
                        "type": i["TipoOferta"],
                        "amount":i["Cantidad"]
                    })
                if i["Foto"] != "":
                    album.photo = "ofertas/" + i["Foto"]
                    album.save()

        # Closing file
        f.close()

def resolve_movie_definition():
    movies = Movie.objects.all()
    for movie in movies:
        if movie.definition is not None:
            movie.definition = movie.definition.upper()
            movie.save()
    return False

def load_data_1():
    errors = False
    try:
        upload_author()
    except Exception as e:
        errors = True
        print("Error uploading authors", e)
    try:
        upload_dvds()
    except Exception as e:
        errors = True
        print("Error uploading dvds", e)
    try:
        upload_albums()
    except Exception as e:
        errors = True
        print("Error uploading albums", e)
    try:
        upload_collection()
    except Exception as e:
        errors = True
        print("Error uploading collections", e)
    try:
        upload_concerts()
    except Exception as e:
        errors = True
        print("Error uploading concerts", e)
    try:
        upload_songs_collection()
    except Exception as e:
        errors = True
        print("Error uploading songs_collection", e)
    
    return errors


def load_data_2():
    errors = False
    try:
        upload_actor()
    except Exception as e:
        errors = True
        print("Error uploading actors", e)
    try:
        upload_movie()
    except Exception as e:
        errors = True
        print("Error uploading movies", e)
    try:
        upload_series()
    except Exception as e:
        errors = True
        print("Error uploading series", e)
    try:
        upload_series_seasons()
    except Exception as e:
        errors = True
        print("Error uploading seasons", e)
    try:
        upload_actor_movie()
    except Exception as e:
        errors = True
        print("Error uploading actor_movie", e)
    try:
        upload_actor_series()
    except Exception as e:
        errors = True
        print("Error uploading actor_series", e)
    return errors


def load_data_3():
    errors = False
    try:
        upload_games()
    except Exception as e:
        errors = True
        print("Error uploading games", e)
    try:
        upload_sports()
    except Exception as e:
        errors = True
        print("Error uploading sports", e)
    try:
        upload_documental()
    except Exception as e:
        errors = True
        print("Error uploading documentals", e)
    try:
        upload_documental_seasons()
    except Exception as e:
        errors = True
        print("Error uploading documental_seasons", e)
    try:
        upload_combos()
    except Exception as e:
        errors = True
        print("Error uploading combos", e)
    try:
        upload_offers()
    except Exception as e:
        errors = True
        print("Error uploading offers", e)
    return errors
    
def load_data_view(request):
    return render(request, "pages/upload_data.html", context={"errors": False})
    
def load_data1_view(request):
    errors = False #load_data_1()
    try:
        print("-------------------------------------")
        update_movie_definition()
        print("-------------------------------------")
    except Exception as e:
        errors = True
        print("Error uploading author", e)

    if errors:
        print("ooooooooooooooooooooooooooooooooooooooo")
        return render(request, "pages/upload_data.html", context={"errors": "At least one error occurred while loading the data, see the logs for more details."})
    else:
        return render(request, "pages/upload_data.html", context={"errors": errors })


def load_data2_view(request):
    errors = load_data_2()
    if errors:
        return render(request, "pages/upload_data.html", context={"errors": "At least one error occurred while loading the data, see the logs for more details."})
    else:
        return render(request, "pages/upload_data.html", context={"errors": errors })


def load_data3_view(request):
    # errors = load_data_3()
    errors = resolve_movie_definition()
    
    if errors:
        return render(request, "pages/upload_data.html", context={"errors": "At least one error occurred while loading the data, see the logs for more details."})
    else:
        return render(request, "pages/upload_data.html", context={"errors": errors })

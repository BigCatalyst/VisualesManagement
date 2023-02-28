from actor.models import Actor
from django.db import models
from django_countries.fields import CountryField
from config.Utiles.UtilidadesBD import *


class Movie(models.Model):
    DEFINITION_CHOICES = (
        ("HD", "HD"),
        ("FULL-HD", "FULL-HD"),
    )
    LANGUAGE_CHOICES = (
        ("Subt-Esp", "Subt-Esp"),
        ("Español", "Español"),
    )
    id = models.AutoField(db_column="Id", primary_key=True)
    title_eng = models.CharField(
        max_length=500, db_column="NombreIng", verbose_name="Título en Inglés")
    title = models.CharField(max_length=500, db_column="Nombre", blank=True,
                             null=True, verbose_name="Título en Español")
    gender = models.ForeignKey(
        "Gender", db_column="Genero",
        blank=True, null=True,
        to_field="name", verbose_name="Género",
        on_delete=models.SET_NULL,
    )
    sub_gender = models.CharField(
        max_length=500, db_column="Subgenero", blank=True, null=True,
        verbose_name="Subgéneros"
    )
    duration = models.CharField(
        max_length=500, db_column="Duracion", blank=True, null=True,
        verbose_name="Duración"
    )
    year = models.IntegerField(db_column="Anno", blank=True, null=True,
                               verbose_name="Año")
    origen = models.CharField(max_length=500, db_column="Origen", default="USA", verbose_name="País de origen")
    format = models.ForeignKey(
        "Format", db_column="Formato",
        to_field="format", verbose_name="Formato", null=True,
        on_delete=models.SET_NULL,
    )
    synopsis = models.TextField(db_column="Sinopsis", blank=True, null=True,
                                verbose_name="Sinopsis")
    saga = models.ForeignKey(
        "Sagas", db_column="Saga",
        blank=True, to_field="title", verbose_name="Saga",
        null=True, on_delete=models.SET_NULL,
    )
    photo = models.ImageField(db_column="FotoPelicula", blank=True,
                              null=True, verbose_name="Foto", max_length=2500,
                              upload_to="peliculas/")
    definition = models.CharField(choices=DEFINITION_CHOICES,
        max_length=500, db_column="Definicion", blank=True, null=True,
        verbose_name="Definicion"
    )
    language = models.CharField(choices=LANGUAGE_CHOICES,
        max_length=500, db_column="Idioma", blank=True, null=True,
        verbose_name="Idioma"
    )
    actor = models.ManyToManyField(Actor, blank=True,
                                   verbose_name="Elenco de la película")
    imdb = models.BooleanField(default=False, null=True, blank=True)
    film_affinity = models.BooleanField(default=False, null=True, blank=True)
    reviewed = models.BooleanField(default=True)

    class Meta:
        app_label = "movie"
        db_table = "peliculas"
        verbose_name = "Película"
        verbose_name_plural = "Películas"

    def __str__(self):
        return self.title_eng

    def save(self, *args, **kwargs):
        self.title = self.title.strip().rstrip() if self.title else None
        self.title_eng = self.title_eng.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class Sport(models.Model):
    DEFINITION_CHOICES = (
        ("HD", "HD"),
        ("FULL-HD", "FULL-HD"),
    )
    
    id = models.AutoField(db_column="Id", primary_key=True)
    name = models.CharField(max_length=500, db_column="Nombre", verbose_name="Nombre")
    year = models.CharField(max_length=500, db_column="Año", blank=True,
                            null=True, verbose_name="Año")
    definition = models.CharField(choices=DEFINITION_CHOICES,
        max_length=500, db_column="Definicion", blank=True, null=True,
        verbose_name="Definición"
    )
    photo = models.ImageField(db_column="Foto", blank=True, null=True,
                              verbose_name="Foto", upload_to="deporte/",
                              max_length=2500,)
    format = models.ForeignKey(
        "Format", db_column="Formato",
        blank=True, null=True,
        to_field="format", verbose_name="Formato",
        on_delete=models.SET_NULL,
    )

    class Meta:
        app_label = "movie"
        db_table = "deportes"
        ordering = ("name",)
        verbose_name = "Deporte"
        verbose_name_plural = "Deportes"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class Documental(models.Model):
    DEFINITION_CHOICES = (
        ("HD", "HD"),
        ("FULL-HD", "FULL-HD"),
    )
    LANGUAGE_CHOICES = (
        ("Subt-Esp", "Subt-Esp"),
        ("Español", "Español"),
    )
    id = models.AutoField(db_column="Id", primary_key=True)
    title_eng = models.CharField(
        max_length=500, db_column="NombreIng", verbose_name="Título en Inglés"
    )
    title = models.CharField(max_length=500, db_column="Nombre", blank=True,
                             null=True, verbose_name="Título en Español")
    gender = models.ForeignKey(
        "GenderDocumental", models.SET_NULL, db_column="Genero", blank=True,
        null=True, verbose_name="Género"
    )
    duration = models.CharField(
        max_length=500, db_column="Duracion", blank=True, null=True,
        verbose_name="Duración"
    )
    year = models.IntegerField(db_column="Anno", blank=True, null=True,
                               verbose_name="Año")
    origen = models.CharField(max_length=500, db_column="Origen", default="USA", verbose_name="País de origen")
    format = models.ForeignKey(
        "Format", db_column="Formato",
        blank=True, null=True,
        to_field="format", verbose_name="Formato",
        on_delete=models.SET_NULL,
    )
    synopsis = models.TextField(db_column="Sinopsis", blank=True, null=True, verbose_name="Sinopsis")
    photo = models.ImageField(db_column="FotoDocumental", blank=True,
                              null=True, verbose_name="Foto",
                              upload_to="documental/", max_length=2500)
    definition = models.CharField(choices=DEFINITION_CHOICES,
        max_length=500, db_column="Definicion", blank=True, null=True,
        verbose_name="Definición"
    )
    language = models.CharField(choices=LANGUAGE_CHOICES,
        max_length=500, db_column="Idioma", blank=True, null=True,
        verbose_name="Idioma"
    )
    type = models.CharField(
        max_length=500, db_column="TipoDocumental", blank=True, null=True,
        verbose_name="Tipo"
    )

    class Meta:
        app_label = "movie"
        db_table = "documental"
        verbose_name = "Documental"
        verbose_name_plural = "Documentales"
        ordering = ("title_eng", )

    def __str__(self):
        return self.title_eng

    def save(self, *args, **kwargs):
        self.title = self.title.strip().rstrip() if self.title else None
        self.title_eng = self.title_eng.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class DocumentalSeason(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    documental = models.ForeignKey(
        Documental, models.SET_NULL, db_column="IdDocumental", blank=True,
        null=True
    )
    season = models.CharField(
        max_length=500, db_column="Temporada", blank=True, null=True,
        verbose_name="Temporada"
    )
    chapters = models.CharField(
        max_length=500, db_column="Capitulos", blank=True, null=True,
        verbose_name="Capítulos"
    )
    year = models.CharField(max_length=500, db_column="Anno", blank=True,
                            null=True, verbose_name="Año")

    class Meta:
        app_label = "movie"
        db_table = "documentalestemporadas"
        verbose_name = "Temporada del Documental"
        verbose_name_plural = "Temporadas del Documental"

    def __str__(self):
        return f"Documental-{self.documental.title_eng}-Temporada-{self.season}"
    def save(self, *args, **kwargs):
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class Format(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    format = models.CharField(
        max_length=500, db_column="Formato", unique=True, verbose_name="Formato"
    )

    class Meta:
        app_label = "movie"
        db_table = "formatos"
        verbose_name = "Formato"
        verbose_name_plural = "Formatos"

    def __str__(self):
        return self.format

    def save(self, *args, **kwargs):
        self.format = self.format.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class GenderDocumental(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    gender = models.ForeignKey(
        "Gender", verbose_name="Género",
        db_column="Genero",
        blank=True,
        null=True,
        to_field="name",
        on_delete=models.SET_NULL,
    )
    photo = models.ImageField(
        upload_to="generos/Documental/", db_column="FotoGenero", blank=True,
        null=True, verbose_name="Foto", max_length=2500
    )
    type = models.CharField(verbose_name="Tipo",
        max_length=500, db_column="TipoDocumental", blank=True, null=True
    )

    class Meta:
        app_label = "movie"
        db_table = "generodocumental"
        ordering = ("type",)
        verbose_name = "Género Documental"
        verbose_name_plural = "Géneros Documentales"

    def __str__(self):
        return self.type.lower()
    def save(self, *args, **kwargs):
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class Gender(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    name = models.CharField(
        verbose_name="Género",
        max_length=500, db_column="Genero", unique=True
    )
    photo = models.ImageField(
        verbose_name="Foto", max_length=2500,
        db_column="FotoGenero", upload_to="generos/", blank=True, null=True
    )

    class Meta:
        app_label = "movie"
        db_table = "generos"
        ordering = ("name",)
        verbose_name = "Género"
        verbose_name_plural = "Géneros"

    def __str__(self):
        return self.name.lower().replace(" ", "-")

    def save(self, *args, **kwargs):
        self.name = self.name.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class Humor(models.Model):
    DEFINITION_CHOICES = (
        ("HD", "HD"),
        ("FULL-HD", "FULL-HD"),
    )
    id = models.AutoField(db_column="Id", primary_key=True)
    title = models.CharField(max_length=500, db_column="Nombre", blank=True,
                             null=True, verbose_name="Título en Español")
    title_eng = models.CharField(
        max_length=500, db_column="NombreIng", verbose_name="Título en Inglés"
    )
    interpreter = models.CharField(
        verbose_name="Intérprete",
        max_length=500, db_column="Interprete", blank=True, null=True
    )
    origen = models.CharField(max_length=500, db_column="Origen", default="USA", verbose_name="País de origen")
    year = models.CharField(max_length=500, db_column="Anno", blank=True,
                            null=True, verbose_name="Año")
    definition = models.CharField(choices=DEFINITION_CHOICES,
        max_length=500, db_column="Definicion", blank=True, null=True,
        verbose_name="Definición"
    )
    photo = models.ImageField(db_column="Foto", blank=True, null=True,
                              verbose_name="Foto", upload_to="humor/", max_length=2500)

    class Meta:
        app_label = "movie"
        db_table = "humor"
        ordering = ("title_eng",)
        verbose_name = "Humor"
        verbose_name_plural = "Humor"

    def __str__(self):
        return self.title_eng

    def save(self, *args, **kwargs):
        self.title = self.title.strip().rstrip() if self.title else None
        self.title_eng = self.title_eng.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class Combo(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    name = models.CharField(max_length=500, db_column="Combo", verbose_name="Nombre")
    photo = models.ImageField(db_column="FotoCombo", blank=True, null=True,
                              verbose_name="Foto", upload_to="combos/", max_length=2500)

    class Meta:
        app_label = "movie"
        db_table = "combos"
        verbose_name = "Combo"
        verbose_name_plural = "Combos"
        ordering = ("name", )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class ComboMovie(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    combo = models.ForeignKey(
        Combo, models.CASCADE, db_column="IdCombo")
    title = models.CharField(max_length=500, db_column="Titulo", verbose_name="Título")
    description = models.TextField(db_column="Descripcion", blank=True,
                                   null=True, verbose_name="Descripción")

    class Meta:
        app_label = "movie"
        db_table = "peliculascombos"
        verbose_name = "Película del Combo"
        verbose_name_plural = "Películas del Combo"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class Sagas(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    title = models.CharField(
        max_length=500, db_column="Saga", unique=True, verbose_name="Título"
    )

    class Meta:
        app_label = "movie"
        db_table = "sagas"
        ordering = ("title",)
        verbose_name = "Saga"
        verbose_name_plural = "Sagas"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)

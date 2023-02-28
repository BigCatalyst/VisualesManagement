from actor.models import Actor
from django.db import models
from movie.models import Format, Gender
from django_countries.fields import CountryField
from config.Utiles.UtilidadesBD import *

class Serial(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    type = models.CharField(max_length=500, db_column="Tipo", blank=True,
                            null=True, verbose_name="Tipo")
    title = models.CharField(max_length=1000, db_column="Titulo", blank=True,
                             null=True, verbose_name="Título en Español")
    title_eng = models.CharField(
        max_length=1000, db_column="TituloIng", verbose_name="Título en Inglés"
    )
    gender = models.ForeignKey(
        Gender, verbose_name="Género",
        to_field="name",
        db_column="Genero",
        on_delete=models.CASCADE,
    )
    origen = models.CharField(max_length=500, db_column="Origen", default="USA", verbose_name="País de origen")
    synopsis = models.TextField(
        db_column="Sinopsis", blank=True, null=True,
        verbose_name="Sinopsis"
    )
    photo = models.ImageField(db_column="FotoSerie", blank=True, null=True,
                              verbose_name="Foto", upload_to="series/",
                              max_length=2500)
    initial = models.CharField(
        max_length=500, db_column="Inicial", blank=True, null=True
    )
    in_transmission = models.BooleanField(db_column="EnCurso", blank=True,
                                          null=True, verbose_name="En curso")
    actor = models.ManyToManyField(Actor, blank=True,
                                   verbose_name="Elenco")
    imdb = models.BooleanField(default=False, null=True, blank=True)
    film_affinity = models.BooleanField(default=False, null=True, blank=True)
    reviewed = models.BooleanField(default=True)

    class Meta:
        app_label = "serial"
        db_table = "series"
        verbose_name = "Serie"
        verbose_name_plural = "Series"

    def __str__(self):
        return self.title_eng

    def save(self, *args, **kwargs):
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class Season(models.Model):
    DEFINITION_CHOICES = (
        ("HD", "HD"),
        ("FULL-HD", "FULL-HD"),
    )
    LANGUAGE_CHOICES = (
        ("Subt-Esp", "Subt-Esp"),
        ("Español", "Español"),
    )
    id = models.AutoField(db_column="Id", primary_key=True)
    number = models.CharField(
        max_length=500, db_column="Temporada", verbose_name="Temporada"
    )
    chapters = models.CharField(
        max_length=500, db_column="Capitulos", blank=True, null=True,
        verbose_name="Capítulos"
    )
    definition = models.CharField(choices=DEFINITION_CHOICES,
        max_length=500, db_column="Definicion", blank=True, null=True,
        verbose_name="Definición"
    )
    series = models.ForeignKey(Serial, models.CASCADE, db_column="IdSerie")
    year = models.CharField(max_length=500, db_column="Anno", blank=True,
                            null=True, verbose_name="Año")
    format = models.ForeignKey(
        Format,
        db_column="Formato",
        default="No",
        to_field="format",
        on_delete=models.CASCADE,
    )
    language = models.CharField(choices=LANGUAGE_CHOICES,
        max_length=500, db_column="Idioma", blank=True, null=True,
        verbose_name="Idioma"
    )

    class Meta:
        app_label = "serial"
        db_table = "seriestemporadas"
        ordering = ("number",)
        verbose_name = "Temporada de la serie"
        verbose_name_plural = "Temporadas de la serie"

    def __str__(self):
        return f"Serie-{self.series.title_eng}-Temporada-{self.number}"
    def save(self, *args, **kwargs):
        setID_Siguiente(self)
        super().save(*args, **kwargs)

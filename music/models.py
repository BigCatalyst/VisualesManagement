from django.db import models
from django.db.models import F

from movie.models import Format
from config.Utiles.UtilidadesBD import *

class Author(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    name = models.CharField(
        verbose_name="Nombre",
        max_length=500, db_column="Nombre", unique=True
    )
    photo = models.ImageField(db_column="Foto", blank=True, null=True,
                              verbose_name="Foto", upload_to="discografia/", max_length=2500)

    class Meta:
        app_label = "music"
        db_table = "autors"
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ("name", )

    def __str__(self):
        return self.name
        
    @property
    def total_albums(self):
        return self.album_set.count()
    
    @property
    def total_dvds(self):
        return self.dvd_set.count()

    def save(self, *args, **kwargs):
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class Album(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    title = models.CharField(max_length=500, db_column="Titulo",
                             verbose_name="Título")
    year = models.IntegerField(db_column="Anno", blank=True, null=True,
                               verbose_name="Año")
    photo = models.ImageField(db_column="Foto", blank=True, null=True,
                              verbose_name="Foto", upload_to="album/", max_length=2500)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, db_column="IdAutor",
        verbose_name="Autor"
    )
    author_navigation_id = models.IntegerField(
        db_column="IdAutorNavigationId", blank=True, null=True
    )
    photo_back = models.ImageField(db_column="FotoBack", blank=True,
                                   null=True, verbose_name="Foto posterior",
                                   upload_to="album/", max_length=2500)

    class Meta:
        app_label = "music"
        db_table = "albums"
        ordering = (F("year").desc(nulls_last=True), "title")
        verbose_name = "Album"
        verbose_name_plural = "Albums"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.strip().rstrip()
        setID_Siguiente(self)
        super(Album, self).save(*args, **kwargs)


class Concert(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    interpreter = models.CharField(
        max_length=500, db_column="Interprete", verbose_name="Intérprete"
    )
    place = models.CharField(max_length=500, db_column="Lugar", blank=True,
                             null=True, verbose_name="Lugar")
    year = models.IntegerField(db_column="Anno", blank=True, null=True,
                               verbose_name="Año")
    definition = models.CharField(
        max_length=500, db_column="Definicion", blank=True, null=True,
        verbose_name="Definición"
    )
    photo = models.ImageField(db_column="Foto", blank=True, null=True,
                              verbose_name="Foto", upload_to="concierto/", max_length=2500)

    class Meta:
        app_label = "music"
        db_table = "conciertos"
        verbose_name = "Concierto"
        verbose_name_plural = "Conciertos"
        ordering = ("interpreter", )

    def __str__(self):
        return self.interpreter

    def save(self, *args, **kwargs):
        self.interpreter = self.interpreter.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class AlbumSong(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    title = models.CharField(max_length=500, db_column="Titulo",
                             verbose_name="Título")
    album = models.ForeignKey(
        Album, models.CASCADE, db_column="IdAlbum"
    )

    class Meta:
        app_label = "music"
        db_table = "cancionalbums"
        verbose_name = "Canción del Album"
        verbose_name_plural = "Canciones del Album"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class DVD(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    title = models.CharField(max_length=500, db_column="Titulo",
                             verbose_name="Título")
    author = models.ForeignKey(
        Author, verbose_name="Autor",
        db_column="Autor",
        to_field="name",
        on_delete=models.CASCADE,
    )
    year = models.IntegerField(db_column="Anno", blank=True, null=True,
                               verbose_name="Año")
    photo = models.ImageField(db_column="Foto", blank=True, null=True,
                              verbose_name="Foto", upload_to="dvd/", max_length=2500)
    photo_back = models.ImageField(db_column="FotoBack", blank=True,
                                   null=True, verbose_name="Foto posterior",
                                   upload_to="dvd/", max_length=2500)

    class Meta:
        app_label = "music"
        db_table = "dvd"
        verbose_name = "DVD"
        verbose_name_plural = "DVDs"
        ordering = ("title", )

    def save(self, *args, **kwargs):
        self.title = self.title.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class DVDSong(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    dvd = models.ForeignKey(
        DVD, models.CASCADE, db_column="IdDvd"
    )
    title = models.CharField(max_length=500, db_column="Nombre",
                             verbose_name="Título")

    class Meta:
        app_label = "music"
        db_table = "canciondvd"
        verbose_name = "Canción del DVD"
        verbose_name_plural = "Canciones del DVD"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class GenderMusic(models.Model):
    name = models.CharField(max_length=500, unique=True, verbose_name="Nombre")
    photo = models.ImageField(upload_to="generosmusica/", null=True,
                              blank=True, verbose_name="Foto", max_length=2500)

    class Meta:
        app_label = "music"
        ordering = ("name",)
        verbose_name = "Género Musical"
        verbose_name_plural = "Géneros Musicales"

    def __str__(self):
        return self.name.lower()

    def save(self, *args, **kwargs):
        self.name = self.name.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class Collection(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    gender = models.ForeignKey(
        GenderMusic,
        to_field="name",
        on_delete=models.CASCADE,
        db_column="Genero",
        verbose_name="Género"
    )
    name = models.CharField(max_length=500, db_column="Nombre",
                            verbose_name="Nombre")
    format = models.ForeignKey(
        Format,
        db_column="Formato",
        to_field="format",
        on_delete=models.CASCADE,
        verbose_name="Formato"
    )
    photo = models.ImageField(db_column="Foto", blank=True, null=True,
                              verbose_name="Foto", upload_to="coleccion/",
                              max_length=2500)

    class Meta:
        app_label = "music"
        db_table = "coleccions"
        verbose_name = "Colección"
        verbose_name_plural = "Colecciones"
        ordering = ("name", )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)

    @property
    def total_songs(self):
        return self.song_set.count()

class Song(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    title = models.CharField(
        max_length=500, db_column="TituloCancion", verbose_name="Título"
    )
    success = models.BooleanField(db_column="Exito", default=False, blank=True, null=True,
                                  verbose_name="Éxito")
    video = models.BooleanField(db_column="Video", default=False, blank=True, null=True)
    collection = models.ForeignKey(
        Collection, models.CASCADE, db_column="IdColeccion",
        verbose_name="Colección"
    )

    class Meta:
        app_label = "music"
        db_table = "cancions"
        ordering = (F("success").desc(nulls_last=True), "title")
        verbose_name = "Canción"
        verbose_name_plural = "Canciones"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)

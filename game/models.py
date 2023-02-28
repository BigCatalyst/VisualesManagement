from django.db import models
from rest_framework.utils import model_meta
from config.Utiles.UtilidadesBD import *

class Category(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    name = models.CharField(max_length=500, db_column="Nombre",
                            verbose_name="Nombre")
    photo = models.ImageField(db_column="FotoCategoria", blank=True,
                              max_length=2500, upload_to="juegos/tarjetas/",
                              null=True, verbose_name="Foto Inicial")
    photo_back = models.ImageField(db_column="FotoCategoriaBack", blank=True,
                              max_length=2500, upload_to="juegos/tarjetas/",
                              null=True, verbose_name="Foto Posterior")

    class Meta:
        app_label = "game"
        db_table = "juegoscategorias"
        ordering = ("name",)
        verbose_name = "Categoría del Juego"
        verbose_name_plural = "Categorías de los Juegos"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)


class Game(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    name = models.CharField(max_length=500, db_column="Nombre",
                            verbose_name="Nombre")
    year = models.IntegerField(db_column="Anno", blank=True, null=True,
                               verbose_name="Año")
    category = models.ForeignKey(
        Category, models.SET_NULL, db_column="IdCategoria", blank=True,
        null=True, verbose_name="Categoría"
    )
    photo = models.ImageField(upload_to="juegos/", db_column="Foto",
                              blank=True, null=True, max_length=2500,
                              verbose_name="Foto")
    manual = models.FileField(upload_to="juegos/manual/",
                              db_column="Manual", blank=True, null=True,
                              max_length=2500
                              )
    synopsis = models.TextField(db_column="Sinopsis", blank=True, null=True,
                                verbose_name="Sinopsis")
    type = models.CharField(max_length=500, db_column="Tipo", blank=True,
                            null=True, verbose_name="Tipo")
    size = models.CharField(max_length=500, db_column="Tamano", blank=True,
                            null=True, verbose_name="Tamaño")
    requirement = models.TextField(db_column="Requisitos", blank=True,
                                   null=True, verbose_name="Requisitos")
    rawg = models.BooleanField(default=False, null=True, blank=True)
    reviewed = models.BooleanField(default=True)

    fillables = [
        "id",
        "name",
        "year",
        "category",
        "photo",
        "manual",
        "synopsis",
        "type",
        "size",
        "requirement",
    ]

    class Meta:
        app_label = "game"
        db_table = "juegos"
        ordering = ("name",)
        verbose_name = "Juego"
        verbose_name_plural = "Juegos"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)

    def fill(self, attributes: {}) -> None:
        """
        Set specified values on current instance
        :param attributes: Dict
        :return: None
        """
        if "category" in attributes and attributes["category"]:
            try:
                attributes["category"] = Category.objects.get(
                    id=attributes["category"])
            except Category.DoesNotExist as err:
                raise err
        for attr_name in attributes:
            fillables = self.fillables
            if not fillables:
                raise NotImplementedError(
                    "There is not specified any field as fillable."
                )

            if attr_name in fillables:
                value = attributes[attr_name]
                setattr(self, attr_name, value)

    @property
    def fields_with_relations(self) -> []:
        """
        Return a tuple with list of fields with any relation (many-to-many or
        one-to-many)
        :return: Tuple
        """

        info = model_meta.get_field_info(self)
        many_to_many = []
        one_to_many = []

        for field_name, relation_info in info.relations.items():
            if relation_info.to_many:
                if relation_info.reverse:
                    one_to_many.append(field_name)
                else:
                    many_to_many.append(field_name)

        return many_to_many, one_to_many


class GameCapture(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE,
                             related_name="captures")
    image = models.ImageField(upload_to="juegos/capturas/", max_length=2500)

    class Meta:
        app_label = "game"
        verbose_name = "Captura del Juego"
        verbose_name_plural = "Capturas del Juego"

    def __str__(self):
        return f"Captura-{self.id}-Juego-{self.game.name}"
    def save(self, *args, **kwargs):
        setID_Siguiente(self)
        super().save(*args, **kwargs)

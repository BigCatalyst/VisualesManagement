from django.db import models
from config.Utiles.UtilidadesBD import *

class Actor(models.Model):
    id = models.AutoField(db_column="Id", primary_key=True)
    name = models.CharField(max_length=500, db_column="Nombre",
                            verbose_name="Nombre y apellidos")
    photo = models.ImageField(db_column="FotoActor", upload_to="actores/",
                              blank=True, null=True, max_length=2500)
    display = models.BooleanField(db_column="Mostrar", blank=True, null=True, verbose_name="Mostrar")
    imdb = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        app_label = "movie"
        db_table = "actors"
        verbose_name = "Actor"
        verbose_name_plural = "Actores"
        ordering = ("name", )

    def save(self, *args, **kwargs):
        self.name = self.name.strip().rstrip()
        setID_Siguiente(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

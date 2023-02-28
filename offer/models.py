from django.db import models
from config.Utiles.UtilidadesBD import *

class Offer(models.Model):
    TYPE_CHOICES = (
        ("0", "Videos"),
        ("1", "Audios"),
        ("2", "Diversos"),
    )
    id = models.AutoField(db_column="Id", primary_key=True)
    amount = models.IntegerField(db_column="Cantidad", blank=True, null=True,
                                 verbose_name="Cantidad")
    name = models.TextField(db_column="Oferta", verbose_name="Oferta")
    price = models.TextField(db_column="Precio", blank=True, null=True,
                             verbose_name="Precio")
    especial = models.CharField(
        max_length=250, db_column="Especial", blank=True, null=True
    )
    description = models.TextField(db_column="Descripcion", blank=True,
                                   null=True, verbose_name="Descripción")
    type = models.CharField(db_column="TipoOferta", blank=True, null=True,
                            verbose_name="Tipo", max_length=250, choices=TYPE_CHOICES,)
    photo = models.ImageField(db_column="Foto", blank=True, null=True,
                              verbose_name="Foto", upload_to="ofertas/",
                              max_length=2500)

    class Meta:
        app_label = "offer"
        db_table = "ofertas"
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        setID_Siguiente(self)
        super().save(*args, **kwargs)

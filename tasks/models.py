from datetime import timedelta

import pgcrypto
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now
from pygments.lexer import default


class License(models.Model):
    license_id = models.CharField(max_length=200, unique=True,
                                  verbose_name="Código de Activación")
    key = models.TextField(verbose_name="LLave de activación")
    created = pgcrypto.EncryptedDateTimeField(default=now)
    expired = pgcrypto.EncryptedDateTimeField(null=True, blank=True)
    validated = pgcrypto.EncryptedDateTimeField(default=now)

    def __str__(self):
        return self.license_id

    class Meta:
        verbose_name = "Licencia"
        ordering = ("-id",)

        
class Contact(models.Model):
    address = models.CharField(max_length=500, verbose_name="Dirección")
    email = models.EmailField(max_length=254, verbose_name="Email")
    phones = ArrayField(models.CharField(max_length=15, blank=True), size=2, verbose_name="Teléfonos", help_text="Teléfonos separados por coma.") 
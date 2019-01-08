from django.db import models


class Empresa(models.Model):
    rfc = models.CharField(max_length=13, null=False, blank=False)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    cer = models.FileField(null=False, blank=False)
    key = models.FileField(null=False, blank=False)
    contrasena = models.CharField(max_length=20, null=False, blank=False)

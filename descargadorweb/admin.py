from django.contrib import admin

from . import models

admin.site.register(models.Empresa)
admin.site.register(models.SolicitudDeDescarga)
admin.site.register(models.VerificacionSolicitudDeDescarga)
admin.site.register(models.PaqueteDeDescarga)

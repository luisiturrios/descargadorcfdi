import uuid
import os

from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.db import models

TIPO_SOLICITUD = (
    ('CFDI', 'CFDI'),
    ('Metadata', 'Metadata'),
)

COD_ESTATUS = (
    (300, 'Usuario no válido'),
    (301, 'XML mal formado'),
    (302, 'Sello mal formado'),
    (303, 'Sello no corresponde con el RFC del solicitante'),
    (304, 'Certificado revocado o caduco'),
    (305, 'Certificado no valido'),
    (5000, 'Solicitud recibida con exito'),
    (5001, 'Tercero no autorizado'),
    (5002, 'Agoto solicitudes de por vida'),
    (5003, 'Tope máximo'),
    (5004, 'No se encontró la información'),
    (5005, 'Solicitud duplicada'),
    (5008, 'Máximo de descargas permitidas'),
    (404, 'Error no encontrado'),
)

ESTADO_SOLICITUD = (
    (1, 'Aceptada'),
    (2, 'En proceso'),
    (3, 'Terminada'),
    (4, 'Error'),
    (5, 'Rechazada'),
    (6, 'Vencida'),
)


def upload_to_efirma(instance, filename):
    path, ext = os.path.splitext(filename)
    return 'Empresa/{}{}'.format(
        uuid.uuid4(),
        ext
    )


def upload_to_paquete(instance, filename):
    path, ext = os.path.splitext(filename)
    return 'PaqueteDeDescarga/{}{}'.format(
        instance.id_paquete,
        ext
    )


class Empresa(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='empresas', null=False, blank=False,
                             on_delete=models.CASCADE)

    rfc = models.CharField(max_length=13, unique=True, null=False, blank=False)

    nombre = models.CharField(max_length=100, null=True, blank=True)

    cer = models.FileField(null=False, blank=False, upload_to=upload_to_efirma,
                           help_text='Ingrese el archivo .cer de su E.firma o Fiel',
                           validators=[FileExtensionValidator(allowed_extensions=['cer'])])

    key = models.FileField(null=False, blank=False, upload_to=upload_to_efirma,
                           help_text='Ingrese el archivo .key de su E.firma o Fiel',
                           validators=[FileExtensionValidator(allowed_extensions=['key'])])

    contrasena = models.CharField(max_length=50, null=False, blank=False,
                                  help_text='Ingrese la contraseña de su E.firma o Fiel')

    not_before = models.DateTimeField(null=False, blank=True)

    not_after = models.DateTimeField(null=False, blank=True)

    # Campos de control interno
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.rfc, self.nombre)

    class Meta:
        ordering = ['-pk']


class SolicitudDeDescarga(models.Model):
    empresa = models.ForeignKey('descargadorweb.Empresa', related_name='solicitudes', null=False, blank=False,
                                on_delete=models.CASCADE)

    id_solicitud = models.UUIDField(unique=True, null=False, blank=False)

    fecha_inicial = models.DateTimeField(null=False, blank=False)

    fecha_final = models.DateTimeField(null=False, blank=False)

    rfc_receptor = models.CharField(max_length=13, null=True, blank=True)

    rfc_emisor = models.CharField(max_length=13, null=True, blank=True)

    tipo_solicitud = models.CharField(max_length=8, null=False, blank=False, choices=TIPO_SOLICITUD)

    cod_estatus = models.PositiveIntegerField(null=False, blank=False, choices=COD_ESTATUS)

    mensaje = models.CharField(null=False, blank=False, max_length=50)

    estado_solicitud = models.PositiveIntegerField(null=True, blank=True, choices=ESTADO_SOLICITUD)

    numero_cfdis = models.PositiveIntegerField(null=True, blank=True, default=None)

    fecha_ultima_verificacion = models.DateTimeField(null=True, blank=True, default=None)
    fecha_resolucion = models.DateTimeField(null=True, blank=True, default=None)

    # Campos de control interno
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id_solicitud)

    class Meta:
        ordering = ['-pk']


class VerificacionSolicitudDeDescarga(models.Model):
    solicitud_de_descarga = models.ForeignKey('descargadorweb.SolicitudDeDescarga', related_name='verificaciones',
                                              null=False, blank=False, on_delete=models.CASCADE)

    fecha_verificacion = models.DateTimeField(null=True, blank=True, default=None)

    cod_estatus = models.PositiveIntegerField(null=False, blank=False, choices=COD_ESTATUS)

    mensaje = models.CharField(null=False, blank=False, max_length=50)

    cod_estatus_solicitud = models.PositiveIntegerField(null=False, blank=False, choices=COD_ESTATUS)

    estado_solicitud = models.PositiveIntegerField(null=False, blank=False, choices=ESTADO_SOLICITUD)

    numero_cfdis = models.PositiveIntegerField(null=True, blank=True, default=None)

    # Campos de control interno
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.solicitud_de_descarga.id_solicitud, self.fecha_verificacion)

    class Meta:
        ordering = ['-pk']


class PaqueteDeDescarga(models.Model):
    solicitud_de_descarga = models.ForeignKey('descargadorweb.SolicitudDeDescarga', related_name='paquetes', null=False,
                                              blank=False, on_delete=models.CASCADE)

    id_paquete = models.CharField(max_length=100, unique=True, null=False, blank=False)

    cod_estatus = models.PositiveIntegerField(null=True, blank=True, choices=COD_ESTATUS)

    mensaje = models.CharField(null=False, blank=False, max_length=50)    

    paqueteb64 = models.FileField(null=True, blank=True, upload_to=upload_to_paquete)

    fecha_descarga = models.DateTimeField(null=True, blank=True, default=None)

    # Campos de control interno
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id_paquete)

    class Meta:
        ordering = ['-pk']

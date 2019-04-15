import base64

from celery.utils.log import get_task_logger
from cfdiclient import (Autenticacion, DescargaMasiva, Fiel,
                        VerificaSolicitudDescarga)
from django.core.files.base import ContentFile
from django.utils import timezone

from descargador import celery_app
from descargadorweb import models

logger = get_task_logger(__name__)


@celery_app.task(bind=True, max_retries=None)
def verificar_solicitud_descarga(self, pk):
    solicitud = models.SolicitudDeDescarga.objects.get(pk=pk, activo=True)

    if solicitud.estado_solicitud and solicitud.estado_solicitud >= 3:
        return 'Solicitud en estado: {}'.format(solicitud.get_estado_solicitud_display())

    cer_der = solicitud.empresa.cer.read()
    key_der = solicitud.empresa.key.read()

    fiel = Fiel(cer_der, key_der, solicitud.empresa.contrasena)

    auth = Autenticacion(fiel)

    token = auth.obtener_token()

    verificador = VerificaSolicitudDescarga(fiel)

    result = verificador.verificar_descarga(token, solicitud.empresa.rfc, str(solicitud.id_solicitud))

    verificacion = models.VerificacionSolicitudDeDescarga()

    verificacion.solicitud_de_descarga = solicitud

    verificacion.fecha_verificacion = timezone.now()

    verificacion.cod_estatus = int(result['cod_estatus'])

    verificacion.mensaje = result['mensaje']

    verificacion.cod_estatus_solicitud = int(result['codigo_estado_solicitud'])

    verificacion.estado_solicitud = int(result['estado_solicitud'])

    verificacion.numero_cfdis = int(result['numero_cfdis'])

    solicitud.cod_estatus = verificacion.cod_estatus_solicitud

    solicitud.estado_solicitud = verificacion.estado_solicitud

    solicitud.fecha_ultima_verificacion = verificacion.fecha_verificacion

    solicitud.numero_cfdis = verificacion.numero_cfdis

    if solicitud.estado_solicitud == 3:
        solicitud.fecha_resolucion = verificacion.fecha_verificacion

        for paq in result['paquetes']:
            paquete = models.PaqueteDeDescarga()
            paquete.solicitud_de_descarga = solicitud
            paquete.id_paquete = paq
            paquete.save()
            descargar_paquete.delay(paquete.pk)

    verificacion.save()

    solicitud.save()

    return True


@celery_app.task(bind=True)
def descargar_paquete(self, pk):
    paquete = models.PaqueteDeDescarga.objects.get(pk=pk, activo=True)

    cer_der = paquete.solicitud_de_descarga.empresa.cer.read()
    key_der = paquete.solicitud_de_descarga.empresa.key.read()

    fiel = Fiel(cer_der, key_der, paquete.solicitud_de_descarga.empresa.contrasena)

    auth = Autenticacion(fiel)

    token = auth.obtener_token()

    descarga_masiva = DescargaMasiva(fiel)

    result = descarga_masiva.descargar_paquete(token, paquete.solicitud_de_descarga.empresa.rfc, paquete.id_paquete)

    paquete.cod_estatus = int(result['cod_estatus'])
    paquete.mensaje = result['mensaje']

    if int(result['cod_estatus']) == 5000:
        paquete.paqueteb64.save('{}.zip'.format(paquete.id_paquete), base64.b64decode(result['paquete_b64']), save=True)
        paquete.fecha_descarga = timezone.now()

    paquete.save()

    return True

from datetime import datetime
import base64

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.views import generic
from django.views import View

from cfdiclient import SolicitaDescarga
from cfdiclient import Autenticacion
from cfdiclient import Fiel

from . import models
from . import tasks
from . import forms


class IndexView(generic.TemplateView):
    template_name = 'descargadorweb/index.html'


class CaracteristicasView(generic.TemplateView):
    template_name = 'descargadorweb/caracteristicas.html'


class ContactoView(generic.FormView):
    template_name = 'descargadorweb/contacto.html'
    form_class = forms.ContactoForm
    success_url = reverse_lazy('descargadorweb:contacto_completo')

    def form_valid(self, form):
        domain = get_current_site(self.request).domain
        subject = 'Mensaje recibido en el sitio {}'.format(domain)

        email = EmailMessage(
            subject=subject,
            body=form.cleaned_data['mensaje'],
            to=[form.cleaned_data['correo'], ],
            bcc=settings.ADMINS,
        )

        # email.send()

        return super().form_valid(form)


class ContactoCompletoView(generic.TemplateView):
    template_name = 'descargadorweb/contacto_completo.html'


class EmpresasView(LoginRequiredMixin, generic.ListView):
    template_name = 'descargadorweb/empresas.html'
    model = models.Empresa

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user, activo=True)
        return queryset


class EmpresasCrearView(LoginRequiredMixin, generic.FormView):
    template_name = 'descargadorweb/empresas_crear.html'
    form_class = forms.EmpresasForm
    success_url = reverse_lazy('descargadorweb:empresas')

    def form_valid(self, form):
        empresa = form.save(commit=False)
        empresa.user = self.request.user
        empresa.save()
        return super().form_valid(form)


class EmpresasDetalleView(LoginRequiredMixin, generic.DetailView):
    model = models.Empresa
    template_name = 'descargadorweb/empresas_detalle.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user, activo=True)
        return queryset


class SolicitudDeDescargaCrearView(LoginRequiredMixin, View):
    template_name = 'descargadorweb/solicitud_de_descarga_crear.html'

    def get(self, request, empresa_pk):
        empresa = get_object_or_404(models.Empresa, pk=empresa_pk, user=self.request.user, activo=True)

        form = forms.SolicitudDeDescargaForm()

        return render(request, self.template_name, {'empresa': empresa, 'form': form})

    def post(self, request, empresa_pk):
        empresa = get_object_or_404(models.Empresa, pk=empresa_pk, user=self.request.user, activo=True)

        form = forms.SolicitudDeDescargaForm(request.POST)

        if form.is_valid():
            try:
                fecha_inicial = form.cleaned_data['fecha_inicial']
                fecha_final = form.cleaned_data['fecha_final']
                tipo = form.cleaned_data['tipo']
                tipo_solicitud = form.cleaned_data['tipo_solicitud']

                fecha_inicial = datetime.combine(fecha_inicial, datetime.min.time())
                fecha_final = datetime.combine(fecha_final, datetime.max.time())

                rfc_emisor = None
                rfc_receptor = None

                if tipo == 'E':
                    rfc_emisor = empresa.rfc
                elif tipo == 'R':
                    rfc_receptor = empresa.rfc

                cer_der = empresa.cer.read()
                key_der = empresa.key.read()

                fiel = Fiel(cer_der, key_der, empresa.contrasena)

                auth = Autenticacion(fiel)

                token = auth.obtener_token()

                descarga = SolicitaDescarga(fiel)

                result = descarga.solicitar_descarga(
                    token, empresa.rfc, fecha_inicial, fecha_final, rfc_emisor=rfc_emisor,
                    rfc_receptor=rfc_receptor, tipo_solicitud=tipo_solicitud
                )

                solicitud = models.SolicitudDeDescarga()

                solicitud.empresa = empresa

                solicitud.id_solicitud = result['id_solicitud']

                solicitud.fecha_inicial = fecha_inicial

                solicitud.fecha_final = fecha_final

                solicitud.rfc_receptor = rfc_receptor

                solicitud.rfc_emisor = rfc_emisor

                solicitud.tipo_solicitud = tipo_solicitud

                solicitud.cod_estatus = int(result['cod_estatus'])

                solicitud.mensaje = result['mensaje']

                solicitud.save()

                return redirect('descargadorweb:solicitud_de_descarga_detalle', empresa_pk=empresa.pk, pk=solicitud.pk)

            except Exception as e:
                form.add_error(None, str(e))

        return render(request, self.template_name, {'empresa': empresa, 'form': form})


class SolicitudDeDescargaDetalleView(LoginRequiredMixin, View):
    template_name = 'descargadorweb/solicitud_de_descarga_detalle.html'

    def get(self, request, empresa_pk, pk):
        empresa = get_object_or_404(models.Empresa, pk=empresa_pk, user=self.request.user, activo=True)

        solicitud = get_object_or_404(models.SolicitudDeDescarga, pk=pk, empresa=empresa, activo=True)

        return render(request, self.template_name, {'empresa': empresa, 'solicitud': solicitud})


class SolicitudDeDescargaVerificarView(LoginRequiredMixin, View):
    def get(self, request, empresa_pk, pk):
        empresa = get_object_or_404(models.Empresa, pk=empresa_pk, user=request.user, activo=True)

        solicitud = get_object_or_404(models.SolicitudDeDescarga, pk=pk, empresa=empresa, activo=True)

        if solicitud.estado_solicitud and solicitud.estado_solicitud >= 3:
            messages.error(request, 'Solicitud ya verificada')
            return redirect('descargadorweb:solicitud_de_descarga_detalle', empresa_pk=empresa.pk, pk=solicitud.pk)

        tasks.verificar_solicitud_descarga(solicitud.pk)

        messages.info(request, 'Verificación programada')

        return redirect('descargadorweb:solicitud_de_descarga_detalle', empresa_pk=empresa.pk, pk=solicitud.pk)


class PaqueteDeDescargaDescargar(View):
    def get(self, request, empresa_pk, pk):
        empresa = get_object_or_404(models.Empresa, pk=empresa_pk, user=request.user, activo=True)

        paquete = get_object_or_404(models.PaqueteDeDescarga, pk=pk, activo=True)

        if paquete.solicitud_de_descarga.empresa_id != empresa.id:
            return HttpResponseForbidden()

        if paquete.fecha_descarga is None:
            messages.info(request, 'Espere unos segundos a que nuestro sistema descarge su paquete')

            return redirect('descargadorweb:solicitud_de_descarga_detalle', empresa_pk=empresa.pk,
                            pk=paquete.solicitud_de_descarga.pk)

        response = HttpResponse(paquete.paqueteb64.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename={}.zip'.format(paquete.id_paquete)
        return response

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings

from . import models
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

        email.send()

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


class EmpresasCrearView(generic.FormView):
    template_name = 'descargadorweb/empresas_crear.html'
    form_class = forms.EmpresasModelForm
    success_url = reverse_lazy('descargadorweb:empresas')

    def form_valid(self, form):
        empresa = form.save(commit=False)
        empresa.user = self.request.user
        empresa.save()
        return super().form_valid(form)

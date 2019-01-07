from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings

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

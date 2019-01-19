from django import forms

from Crypto.PublicKey import RSA
from OpenSSL import crypto
import dateutil.parser

from . import models


class ContactoForm(forms.Form):
    correo = forms.EmailField(required=True, label='Correo Electrónico')
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, }), required=True, label='Mensaje')


class EmpresasModelForm(forms.ModelForm):
    cer = forms.FileField(widget=forms.FileInput(attrs={'accept': '.cer', }))
    key = forms.FileField(widget=forms.FileInput(attrs={'accept': '.key', }))

    class Meta:
        model = models.Empresa
        fields = ['cer', 'key', 'contrasena']

    def clean_cer(self):
        cer_file = self.cleaned_data['cer'].read()

        cer = crypto.load_certificate(crypto.FILETYPE_ASN1, cer_file)

        subject = cer.get_subject()

        if subject.x500UniqueIdentifier is None:
            raise forms.ValidationError(u'Este no es una E.firma valida')

        self.instance.rfc = subject.x500UniqueIdentifier.strip().upper()

        if models.Empresa.objects.filter(rfc=self.instance.rfc).exists():
            raise forms.ValidationError(u'Empresa ya registrada')

        self.instance.nombre = subject.name.strip().upper()

        self.instance.not_after = dateutil.parser.parse(cer.get_notAfter())

        self.instance.not_before = dateutil.parser.parse(cer.get_notBefore())

        return self.cleaned_data['cer']

    def clean_contrasena(self):
        key_file = self.cleaned_data['key'].read()

        contrasena = self.cleaned_data['contrasena']

        try:
            RSA.importKey(key_file, contrasena)
        except Exception:
            raise forms.ValidationError('Contraseña incorrecta')

        return self.cleaned_data['contrasena']

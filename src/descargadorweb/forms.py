from django import forms

from Crypto.PublicKey import RSA
from OpenSSL import crypto
import dateutil.parser

from . import models


class ContactoForm(forms.Form):
    correo = forms.EmailField(required=True, label='Correo Electrónico')
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, }), required=True, label='Mensaje')


class EmpresasForm(forms.ModelForm):
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

        rfc = subject.x500UniqueIdentifier.strip().upper()

        if len(rfc) > 13:
            rfc = rfc[:13].strip()

        self.instance.rfc = rfc

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


class SolicitudDeDescargaForm(forms.Form):
    fecha_inicial = forms.DateField(required=True, widget=forms.DateInput(attrs={'autocomplete': 'off'}))
    fecha_final = forms.DateField(required=True, widget=forms.DateInput(attrs={'autocomplete': 'off'}))
    tipo = forms.ChoiceField(required=True, choices=(('E', 'Emitidos'), ('R', 'Recibidos')))
    tipo_solicitud = forms.ChoiceField(required=True, choices=models.TIPO_SOLICITUD)

    def clean_fecha_final(self):
        fecha_inicial = self.cleaned_data['fecha_inicial']
        fecha_final = self.cleaned_data['fecha_final']

        if fecha_final < fecha_inicial:
            raise forms.ValidationError('La fecha final no puede ser menor que la fecha inicial')

        if (fecha_final - fecha_inicial).days > 365:
            raise forms.ValidationError('Solo puede descargar un año a la vez')

        return fecha_final

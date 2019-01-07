from django import forms


class ContactoForm(forms.Form):
    correo = forms.EmailField(required=True, label='Correo Electrónico')
    mensaje = forms.CharField(widget=forms.Textarea, required=True, label='Mensaje')

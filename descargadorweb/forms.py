from django import forms


class ContactoForm(forms.Form):
    correo = forms.EmailField(required=True, label='Correo Electrónico')
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'rows':4,}), required=True, label='Mensaje')

from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model
from django import forms


class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Contraseña confirmación',
        widget=forms.PasswordInput,
        strip=False,
        help_text='Introduzca la misma contraseña que antes',
    )

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya se encuentra registrado')

        self.instance.username = email

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Los campos de contraseña no coinciden.',
                code='password_mismatch',
            )
        password_validation.validate_password(
            self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()

        return user

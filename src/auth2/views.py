from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth import views
from django.shortcuts import render

from django.views import generic

from auth2 import forms
from auth2 import tasks


class LoginView(views.LoginView):
    redirect_authenticated_user = True
    template_name = 'auth2/login.html'


class LogoutView(views.LogoutView):
    pass


class SignupView(generic.CreateView):
    template_name = 'auth2/signup.html'
    form_class = forms.UserForm
    success_url = reverse_lazy('auth2:signup_done')
    title = 'Registrar usuario'

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        response = super(SignupView, self).form_valid(form)

        protocol = 'https' if self.request.is_secure() else 'http'
        domain = get_current_site(self.request).domain
        tasks.send_user_activation_email.delay(self.object.pk, protocol, domain)

        return response


class SignupDoneView(generic.TemplateView):
    template_name = 'auth2/signup_done.html'
    title = 'Registrar nueva cuenta'

    def get_context_data(self, **kwargs):
        context = super(SignupDoneView, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class SignupConfirmView(generic.View):

    def get(self, request, uidb64, token):

        title = 'Usuario activado con exito'
        validlink = False

        if uidb64 is not None and uidb64 is not None:

            pk = urlsafe_base64_decode(uidb64)
            user = get_user_model().objects.get(pk=pk)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                validlink = True

        return render(request, 'auth2/signup_confirm.html', {'validlink': validlink, 'title': title})


class PasswordResetView(views.PasswordResetView):
    template_name = "auth2/password_reset.html"
    email_template_name = "auth2/password_reset_email.txt"
    subject_template_name = "auth2/password_reset_email_subject.txt"
    success_url = reverse_lazy('auth2:password_reset_done')


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'auth2/password_reset_done.html'


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'auth2/password_reset_confirm.html'
    success_url = reverse_lazy('auth2:password_reset_complete')


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'auth2/password_reset_complete.html'

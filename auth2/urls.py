from django.urls import path

from auth2 import views

app_name = 'auth2'

urlpatterns = [
    path(
        r'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        r'logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        r'signup/',
        views.SignupView.as_view(),
        name='signup'
    ),
    path(
        r'signup/done/',
        views.SignupDoneView.as_view(),
        name='signup_done'
    ),
    path(
        r'signup/confirm/<uidb64>/<token>/',
        views.SignupConfirmView.as_view(),
        name='signup_confirm'
    ),
    path(
        r'password/reset/',
        views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        r'password/reset/done/',
        views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        r'password/reset/confirm/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        r'password/reset/complete/',
        views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes


from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task()
def send_user_activation_email(user_pk, protocol, domain):

    user = get_user_model().objects.get(pk=user_pk)

    if user.email is None:
        return False

    token = default_token_generator.make_token(user)

    uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()

    context = {
        'user': user,
        'token': token,
        'uid': uid,
        'protocol': protocol,
        'domain': domain,
    }

    subject = 'Confirme su correo electrónico - {}'.format(domain)

    body = get_template('auth2/signup_email.txt').render(context)

    msg = EmailMultiAlternatives(subject=subject, body=body, to=[user.email])

    msg.send()

    return True

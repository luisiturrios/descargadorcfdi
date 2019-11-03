# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'postmaster@descargadorcfdi.com'
EMAIL_HOST_PASSWORD = '1741a27fe11bac89011a0787a42fb230-816b23ef-2f775d4a'
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'Descargador CFDI<no-reply@descargadorcfdi.com>'

# DEBUG
SERVER_EMAIL = 'Descargador CFDI<no-reply@descargadorcfdi.com>'
ADMINS = [('Luis Iturrios', 'iturrios3063@gmail.com')]
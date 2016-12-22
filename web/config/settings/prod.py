from .base import *
from .secret import Secret

DEBUG=False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = Secret.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = Secret.EMAIL_HOST_PASSWORD

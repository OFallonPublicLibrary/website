from .base import *

DEBUG=True
INSTALLED_APPS = ['debug_toolbar'] + INSTALLED_APPS
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
INTERNALIPS = ['127.0.0.1']

# Dirty hack to force toolbar display
def show_toolbar(request):
    return True
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}

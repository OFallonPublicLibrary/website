from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import smart_str

from wagtail.wagtailadmin import messages
from wagtail.wagtailcore.models import Page
from .models import get_events_for_user

def index(request):
    return render(request, 'calendar/index.html', {

    })

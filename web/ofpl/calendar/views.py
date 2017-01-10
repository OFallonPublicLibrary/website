import datetime

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import smart_str

from wagtail.wagtailadmin import messages
from wagtail.wagtailcore.models import Page
from .models import Event, Occurrence, EventType
from .permissions import permission_policy

def index(request, year=None, month=None):
    dt = datetime.datetime.now()
    year = year or dt.year
    month = month or dt.month
    dateobj = datetime.date(year, month, 15)

    return render(request, 'calendar/index.html', {
        'year': year,
        'month': month,
        'datetime': dateobj,
        'monthyear_heading': dateobj.strftime('%B - %Y'),
        'user_can_add': permission_policy['occurrence'].user_has_permission(request.user, 'add'),
    })

def add(request):
    pass

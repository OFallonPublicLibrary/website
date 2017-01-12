import calendar
import itertools
from datetime import datetime, timedelta, time

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse
from django.utils import timezone

from wagtail.wagtailadmin import messages
from wagtail.wagtailcore.models import Page

from .models import Event, Occurrence, EventType
from .permissions import permission_policy
from .conf import settings as calendar_settings
from .forms import SingleOccurrenceForm
from .batch_form import MultipleOccurrenceForm
from . import utils

from dateutil import parser


if calendar_settings.CALENDAR_FIRST_WEEKDAY is not None:
    calendar.setfirstweekday(calendar_settings.CALENDAR_FIRST_WEEKDAY)

TODAY = timezone.now()


def month_view(request, year, month, template='calendar/month_view.html', queryset=None):
    year, month = int(year), int(month)
    cal = calendar.monthcalendar(year, month)
    dtstart = datetime(year, month, 1)
    last_day = max(cal[-1])
    dtend = datetime(year, month, last_day)

    queryset = queryset._clone() if queryset is not None else Occurrence.objects.select_related()
    occurrences = queryset.filter(start_time__year=year, start_time__month=month)

    def start_day(o):
        return o.start_time.day

    by_day = dict([(dt, list(o)) for dt,o in itertools.groupby(occurrences, start_day)])
    data = {
        'today': timezone.now(),
        'calendar': [[(d, by_day.get(d, [])) for d in row] for row in cal],
        'this_month': dtstart,
        'next_month': dtstart + timedelta(days=+last_day),
        'last_month': dtstart + timedelta(days=-1),
        'monthyear_heading': dtstart.strftime('%B | %Y'),
        'user_can_add': permission_policy['occurrence'].user_has_permission(request.user, 'add'),
    }

    return render(request, template, data)


def index(request, year=None, month=None):
    dt = timezone.now()

    if(year == None and month == None):
        year = int(year or dt.year)
        month = int(month or dt.month)
        return month_view(request, year, month)

    elif(year is not None and month == None):
        year = int(year)
        return year_view(request, year)

    else:
        year = int(year)
        month = int(month)
        return month_view(request, year, month)

    thismonth = datetime.date(year, month, 15)


    _last = calendar.monthrange(year, month)[1]
    _first_day = datetime.datetime(year, month, 1)
    _last_day = datetime.datetime(year, month, _last).replace(hour=23, minute=59, second=59)
    calendar_items = Occurrence.objects.filter(
        start_time__gte=_first_day,
        start_time__lt=_last_day,
    ).select_related('event')

    return render(request, 'calendar/index.html', {
        'year': year,
        'month': month,
        'nextmonth': thismonth + datetime.timedelta(30),
        'previousmonth': thismonth - datetime.timedelta(30),
        'monthyear_heading': thismonth.strftime('%B | %Y'),
        'calendar_items': calendar_items,
        'user_can_add': permission_policy['occurrence'].user_has_permission(request.user, 'add'),
    })

def add(request, year=TODAY.year, month=TODAY.month, day=TODAY.day):
    if request.method == 'POST':
        form = SingleOccurrenceForm(request.POST, request.FILES)
        if form.is_valid():
            theoccurrence = form.save()

            messages.success(request, "Event occurrence added", buttons=[
                messages.button(reverse('calendar_occurrence_modeladmin_edit', args=(theoccurrence.id,)), 'Edit')
            ])
            return redirect('calendar:index')
        else:
            messages.error(request, "The occurrence could not be created due to errors.")
    else:
        year,month,day = int(year),int(month),int(day)
        stobj = datetime(year, month, day, TODAY.hour)
        endobj = datetime(year, month, day, TODAY.hour+1)
        initial = {'start_time':stobj, 'end_time':endobj}
        form = SingleOccurrenceForm(initial=initial)

    return render(request, "calendar/add.html", {
        'form': form
    })


def batch_add(request, template='calendar/batch_add.html'):
    dtstart = None
    if request.method == 'POST':
        form = MultipleOccurrenceForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Event occurrence batch added")
            return redirect('calendar:index')
        else:
            messages.error(request, "The occurrence batch could not be created due to errors.")

    else:
        dtstart = timezone.now()
        form = MultipleOccurrenceForm(initial={'dtstart': dtstart})

    return render(
        request,
        template,
        {'dtstart': dtstart, 'form': form}
    )

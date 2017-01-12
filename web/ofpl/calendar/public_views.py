import calendar
import itertools
from datetime import datetime, timedelta, time

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from .conf import settings as calendar_settings
from django.apps import apps

def month_view(event_index_page, request, year, month, queryset=None):
    year, month = int(year), int(month)
    cal = calendar.monthcalendar(year, month)
    dtstart = datetime(year, month, 1)
    last_day = max(cal[-1])
    dtend = datetime(year, month, last_day)

    # Lazy model import to avoid circular import hell
    Occurrence = apps.get_model('calendar', 'Occurrence')

    queryset = queryset._clone() if queryset is not None else Occurrence.objects.select_related()
    occurrences = queryset.filter(start_time__year=year, start_time__month=month)

    def start_day(o):
        return o.start_time.day

    by_day = dict([(dt, list(o)) for dt,o in itertools.groupby(occurrences, start_day)])
    data = {
        'page': event_index_page,
        'today': datetime.now(),
        'calendar': [[(d, by_day.get(d, [])) for d in row] for row in cal],
        'this_month': dtstart,
        'next_month': dtstart + timedelta(days=+last_day),
        'last_month': dtstart + timedelta(days=-1),
        'monthyear_heading': dtstart.strftime('%B | %Y'),
    }

    return render(request, 'calendar/public/month_view.html', data)

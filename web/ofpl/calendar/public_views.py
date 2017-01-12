import calendar
import itertools
from datetime import datetime, timedelta, time

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from .conf import settings as calendar_settings


def month_view(self, request, year, month):
    year, month = int(year), int(month)
    return render('calendar/public/month_view.html', {
        'year': year,
        'month': month,
    })

import calendar
import itertools
from datetime import datetime, timedelta, time

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from .conf import settings as calendar_settings


def this_month(self, request):
    return HttpResponse("Current Month")

def other_month(self, request, year, month):
    return HttpResponse("Different month " + year + " | " + month)

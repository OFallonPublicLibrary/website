from datetime import datetime, date, time, timedelta

from django import forms

from wagtail.wagtailadmin.widgets import AdminDateInput, AdminTimeInput, AdminDateTimeInput
from .models import Event, Occurrence, EventType
from .conf import settings as calendar_settings

def timeslot_options(
    interval=calendar_settings.TIMESLOT_INTERVAL,
    start_time=calendar_settings.TIMESLOT_START_TIME,
    end_delta=calendar_settings.TIMESLOT_END_TIME_DURATION,
    fmt=calendar_settings.TIMESLOT_TIME_FORMAT
):
    '''
    Create a list of time slot options for use in swingtime forms.

    The list is comprised of 2-tuples containing a 24-hour time value and a
    12-hour temporal representation of that offset.

    '''
    dt = datetime.combine(date.today(), time(0))
    dtstart = datetime.combine(dt.date(), start_time)
    dtend = dtstart + end_delta
    options = []

    while dtstart <= dtend:
        options.append((str(dtstart.time()), dtstart.strftime(fmt)))
        dtstart += interval

    return options

#==============================================================

default_timeslot_options = timeslot_options()

#==============================================================
class SplitDateTimeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            SelectDateWidget(attrs=attrs),
            forms.Select(choices=default_timeslot_options, attrs=attrs)
        )
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]

        return [None, None]


class SingleOccurrenceForm(forms.ModelForm):

    required_css_class = "required"

    class Meta:
        model = Occurrence
        fields = ('event', 'display_name_override', 'start_time', 'end_time')
        widgets = {
            'start_time': AdminDateTimeInput,
            'end_time': AdminDateTimeInput,
        }

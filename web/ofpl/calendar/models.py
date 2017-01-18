from datetime import datetime, date, timedelta
from dateutil import rrule

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.utils import timezone

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, FieldRowPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route

from .conf import settings as calendar_settings
from ..cms.models import Skinable
from . import public_views

class EventType(models.Model):
    abbr = models.CharField(_('abbreviation'), max_length=4, unique=True)
    label = models.CharField(_('label'), max_length=50)

    class Meta:
        verbose_name = _('event type')
        verbose_name_plural = _('event types')

    def __str__(self):
        return self.label


class EventRootSingleton(RoutablePageMixin, Page):
    content = RichTextField()

    content_panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('content'),
    ]


class CalendarGridPage(RoutablePageMixin, Page, Skinable):
    content = RichTextField()

    content_panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('page_skin'),
        FieldPanel('content'),
    ]

    @route(r'^$')
    def this_month(self, request):
        dt = timezone.now()
        return public_views.month_view(self, request, dt.year, dt.month)

    @route(r'^(\d+)/(\d+)/$', name='public_calendar')
    def other_month(self, request, year=None, month=None):
        return public_views.month_view(self, request, year, month)


class Event(Page, Skinable):
    type = models.ForeignKey(EventType, verbose_name=_('event type'), on_delete=models.PROTECT)
    what = RichTextField()
    when = RichTextField()
    where = RichTextField()
    who = RichTextField()
    registration_link = models.URLField(blank=True)
    content = RichTextField()

    parent_page_types = [
        EventRootSingleton
    ]

    content_panels = [
        FieldPanel('title', classname='title full'),
        FieldPanel('type'),
        FieldPanel('what'),
        FieldPanel('when'),
        FieldPanel('where'),
        FieldPanel('who'),
        FieldPanel('registration_link'),
        FieldPanel('content'),
        FieldPanel('page_skin'),
        InlinePanel('occurrences', label='Occurrences'),
    ]

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ('title', )

    def __str__(self):
        return self.title

    def add_occurrences(self, start_time, end_time, **rrule_params):
        '''
        Add one or more occurences to the event using a comparable API to
        ``dateutil.rrule``.

        If ``rrule_params`` does not contain a ``freq``, one will be defaulted
        to ``rrule.DAILY``.

        Because ``rrule.rrule`` returns an iterator that can essentially be
        unbounded, we need to slightly alter the expected behavior here in order
        to enforce a finite number of occurrence creation.

        If both ``count`` and ``until`` entries are missing from ``rrule_params``,
        only a single ``Occurrence`` instance will be created using the exact
        ``start_time`` and ``end_time`` values.
        '''
        count = rrule_params.get('count')
        until = rrule_params.get('until')
        if not (count or until):
            self.occurrence_set.create(start_time=start_time, end_time=end_time)
        else:
            rrule_params.setdefault('freq', rrule.DAILY)
            delta = end_time - start_time
            occurrences = []
            for ev in rrule.rrule(dtstart=start_time, **rrule_params):
                occurrences.append(Occurrence(start_time=ev, end_time=ev + delta, event=self))
            self.occurrence_set.bulk_create(occurrences)

    def upcoming_occurrences(self):
        '''
        Return all occurrences that are set to start on or after the current
        time.
        '''
        return self.occurrence_set.filter(start_time__gte=timezone.now())

    def next_occurrence(self):
        '''
        Return the single occurrence set to start on or after the current time
        if available, otherwise ``None``.
        '''
        upcoming = self.upcoming_occurrences()
        return upcoming[0] if upcoming else None

    def daily_occurrences(self, dt=None):
        '''
        Convenience method wrapping ``Occurrence.objects.daily_occurrences``.
        '''
        return Occurrence.objects.daily_occurrences(dt=dt, event=self)


class OccurrenceManager(models.Manager):
    use_for_related_fields = True

    def daily_occurrences(self, dt=None, event=None):
        '''
        Returns a queryset of for instances that have any overlap with a
        particular day.

        * ``dt`` may be either a datetime.datetime, datetime.date object, or
          ``None``. If ``None``, default to the current day.

        * ``event`` can be an ``Event`` instance for further filtering.
        '''
        dt = dt or timezone.now()
        start = datetime(dt.year, dt.month, dt.day)
        end = start.replace(hour=23, minute=59, second=59)
        qs = self.filter(
            models.Q(
                start_time__gte=start,
                start_time__lte=end,
            ) |
            models.Q(
                end_time__gte=start,
                end_time__lte=end,
            ) |
            models.Q(
                start_time__lt=start,
                end_time__gt=end
            )
        )

        return qs.filter(event=event) if event else qs


class Occurrence(models.Model):
    '''
    Represents the start end time for a specific occurrence of a master ``Event``
    object.
    '''
    start_time = models.DateTimeField(_('start time'))
    end_time = models.DateTimeField(_('end time'), null=True, blank=True)
    all_day = models.BooleanField(default=False)
    display_name_override = models.CharField(max_length=255, blank=True)
    event = ParentalKey(Event, verbose_name=_('event'), related_name='occurrences')

    @property
    def display_name(self):
        if self.display_name_override == "":
            return self.event.title
        else:
            return self.display_name_override

    panels = [
        FieldPanel('event'),
        FieldPanel('display_name_override'),
        FieldPanel('all_day'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
    ]

    objects = OccurrenceManager()

    class Meta:
        verbose_name = _('occurrence')
        verbose_name_plural = _('occurrences')
        ordering = ('start_time', 'end_time')

    def __str__(self):
        return '{}: {}'.format(self.title, self.start_time.isoformat())

    def __lt__(self, other):
        return self.start_time < other.start_time

    @property
    def title(self):
        return self.event.title

    @property
    def type(self):
        return self.event.type



# Helper Methods

def create_event(
    title,
    type,
    description='',
    start_time=None,
    end_time=None,
    **rrule_params
):
    '''
    Convenience function to create an ``Event``, optionally create an
    ``EventType``, and associated ``Occurrence``s. ``Occurrence`` creation
    rules match those for ``Event.add_occurrences``.

    Returns the newly created ``Event`` instance.

    Parameters

    ``type``
        can be either an ``EventType`` object or 2-tuple of ``(abbreviation,label)``,
        from which an ``EventType`` is either created or retrieved.

    ``start_time``
        will default to the current hour if ``None``

    ``end_time``
        will default to ``start_time`` plus swingtime_settings.DEFAULT_OCCURRENCE_DURATION
        hour if ``None``

    ``freq``, ``count``, ``rrule_params``
        follow the ``dateutils`` API (see http://labix.org/python-dateutil)

    '''

    if isinstance(type, tuple):
        type, created = EventType.objects.get_or_create(
            abbr=type[0],
            label=type[1]
        )

    event = Event.objects.create(
        title=title,
        description=description,
        type=type
    )

    start_time = start_time or timezone.now().replace(
        minute=0,
        second=0,
        microsecond=0
    )

    end_time = end_time or (start_time + calendar_settings.DEFAULT_OCCURRENCE_DURATION)
    event.add_occurrences(start_time, end_time, **rrule_params)
    return event


class EventStreamPage(Page, Skinable):
    content = RichTextField()
    type = models.ForeignKey(EventType, verbose_name=_('event type'), on_delete=models.PROTECT)

    content_panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('content'),
        FieldPanel('type'),
        FieldPanel('page_skin'),
    ]

    @property
    def upcoming_events(self):
        asdf = Occurrence.objects.select_related('event').exclude(start_time__gt=datetime.now()+timedelta(90))
        for x in asdf:
            print(x)
        return asdf


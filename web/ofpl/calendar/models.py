from django.db import models

from eventtools.models import BaseEvent, BaseOccurrence

class Event(BaseEvent):
    title = models.CharField(max_length=255)


class Occurrence(BaseOccurrence):
    event = models.ForeignKey(Event)

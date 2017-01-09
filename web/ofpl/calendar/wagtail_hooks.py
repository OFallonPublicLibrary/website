from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
from .models import Event, Occurrence, EventType

class EventTypeAdmin(ModelAdmin):
    model = EventType
    menu_label = 'Event Types'
    menu_icon = 'tag'


class EventAdmin(ModelAdmin):
    model = Event
    menu_label = 'Events'
    menu_icon = 'date'


class CalendarAdminGroup(ModelAdminGroup):
    menu_label = 'Calendar'
    menu_icon = 'date'
    menu_order = 200
    items = (EventAdmin, EventTypeAdmin, )


modeladmin_register(CalendarAdminGroup)

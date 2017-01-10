from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission

from wagtail.wagtailadmin.menu import MenuItem, SubmenuMenuItem, Menu
from .menu import calendar_menu
from wagtail.wagtailcore import hooks
from . import urls
from .models import Event, Occurrence, EventType

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^calendar/', include(urls, app_name='calendar', namespace='calendar')),
    ]


@hooks.register('register_permissions')
def register_permissions():
    return Permission.objects.filter(
        content_type__app_label='calendar',
        codename__in=[
            'add_occurrence',
            'change_occurrence',
            'delete_occurrence',
        ],
    )


class CalendarMenuItem(SubmenuMenuItem):
    template = 'calendar/calendar_menu_item.html'


@hooks.register('register_admin_menu_item')
def register_calendar_menu():
    return CalendarMenuItem('Calendar', calendar_menu, classnames='icon icon-date', order=300)


class EventTypeAdmin(ModelAdmin):
    model = EventType
    menu_label = 'Event Types'
    menu_icon = 'tag'

    def register_me(self):
        @hooks.register('register_permissions')
        def register_permissions():
            return self.get_permissions_for_registration()

        @hooks.register('register_calendar_menu_item')
        def register_event_tag():
            return self.get_menu_item()

        @hooks.register('register_admin_urls')
        def register_admin_urls():
            return self.get_admin_urls_for_registration()



#class EventAdmin(ModelAdmin):
#    model = Event
#    menu_label = 'Events'
#    menu_icon = 'date'


#class GridMenuItem(MenuItem):
#    def is_show(self, request):
#        return True


#class CalendarAdminGroup(ModelAdminGroup):
#    menu_label = 'Calendar'
#    menu_icon = 'date'
#    menu_order = 200
#    items = (
#        EventTypeAdmin,
#        EventAdmin,
#        GridMenuItem('Grid View', reverse('calendar:index'),
#            name='calendar', classnames='icon icon-date', order=700)
#        )




EventTypeAdmin().register_me()




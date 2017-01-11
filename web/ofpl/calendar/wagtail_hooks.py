from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission

from wagtail.wagtailadmin.menu import MenuItem, SubmenuMenuItem, Menu
from wagtail.wagtailcore import hooks
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)

from .menu import calendar_menu
from . import urls
from .models import Event, Occurrence, EventType
from .permissions import permission_policy


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
            'add_event_type',
            'change_event_type',
            'delete_event_type',
            'add_event',
            'change_event',
            'delete_event',
        ],
    )


class CalendarGridMenuItem(MenuItem):
    pass


@hooks.register('register_calendar_menu_item')
def register_calendar_grid_menu_item():
    return CalendarGridMenuItem(
        'Calendar Grid', reverse('calendar:index'), classnames='icon icon-date', order=100
    )


class CalendarSubmenuItem(SubmenuMenuItem):
    template = 'calendar/calendar_menu_item.html'


@hooks.register('register_admin_menu_item')
def register_calendar_menu():
    return CalendarSubmenuItem('Calendar', calendar_menu, classnames='icon icon-date', order=200)


class EventTypeAdmin(ModelAdmin):
    model = EventType
    menu_label = 'Event Types'
    menu_icon = 'tag'
    order = 500

    def is_shown(self, request):
        return permission_policy.event_type.user_has_any_permission(
            request.user, ['add', 'change', 'delete']
        )

    def register_me(self):
        @hooks.register('register_permissions')
        def register_permissions():
            return self.get_permissions_for_registration()

        @hooks.register('register_calendar_menu_item')
        def register_event_tag():
            return self.get_menu_item(order=self.order)

        @hooks.register('register_admin_urls')
        def register_admin_urls():
            return self.get_admin_urls_for_registration()



class EventAdmin(ModelAdmin):
    model = Event
    menu_label = 'Events (List)'
    menu_icon = 'list-ul'
    order = 100

    def is_shown(self, request):
        return permission_policy.event.user_has_any_permission(
            request.user, ['add', 'change', 'delete']
        )

    def register_me(self):
        @hooks.register('register_calendar_menu_item')
        def register_event_tag():
            return self.get_menu_item(order=self.order)

        @hooks.register('register_admin_urls')
        def register_admin_urls():
            return self.get_admin_urls_for_registration()


class OccurrenceAdmin(ModelAdmin):
    model = Occurrence
    menu_label = 'Occurrences'
    menu_icon = 'list-ul'
    order = 400

    def is_shown(self, request):
        return True

    def register_me(self):
        @hooks.register('register_calendar_menu_item')
        def register_event_tag():
            return self.get_menu_item(order=self.order)

        @hooks.register('register_admin_urls')
        def register_admin_urls():
            return self.get_admin_urls_for_registration()



EventTypeAdmin().register_me()
EventAdmin().register_me()
OccurrenceAdmin().register_me()

print(OccurrenceAdmin().get_admin_urls_for_registration())

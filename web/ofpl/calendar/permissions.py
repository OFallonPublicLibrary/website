from wagtail.wagtailcore.permission_policies import ModelPermissionPolicy
from .models import Event, Occurrence, EventType

permission_policy = {
    'event': ModelPermissionPolicy(Event),
    'event_type': ModelPermissionPolicy(EventType),
    'occurrence': ModelPermissionPolicy(Occurrence),
}

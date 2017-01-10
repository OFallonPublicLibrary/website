from django.template import Library
from django.template.loader import get_template

register = Library()

@register.inclusion_tag("modeladmin/calendar/grid.html", takes_context=True)
def grid(context):
    return context

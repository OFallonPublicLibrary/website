from django.template import Library
from django.template.loader import get_template
from wagtail.wagtailcore.models import Page

register = Library()

@register.inclusion_tag('cms/subnav.html', takes_context=True)
def subnav(context):
    asdf = context['page'].get_ancestors()
    return {
        'heading': asdf[len(asdf)-1].title,
        'page': context['page'],
        'siblings': Page.objects.descendant_of(asdf[len(asdf)-1])
    }

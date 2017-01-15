from django.template import Library
from django.template.loader import get_template
from wagtail.wagtailcore.models import Page

register = Library()

@register.inclusion_tag('cms/subnav.html', takes_context=True)
def subnav(context):
    print(vars(context['page']))
    page = context['page']
    asdf = page.get_ancestors()
    if page.depth == 4:
        return {
            'heading': asdf[len(asdf)-1].title,
            'page': page,
            'siblings': Page.objects.descendant_of(asdf[len(asdf)-1])
        }
    else:
        return {
            'heading': page.title,
            'page': page,
            'siblings': Page.objects.descendant_of(page)
        }

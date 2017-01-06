from django.http import HttpResponse
from django.views.generic import ListView
from .models import Event, Occurrence

import pprint

def test(request):
    asdf = "<pre><code>"
    for x in Event.objects.all():
        asdf += pprint.pformat(vars(x), indent=4) + "\n"
    asdf += "\n\n" + ("Cake") + "\n\n"
    for x in Occurrence.objects.all():
        asdf += pprint.pformat(vars(x), indent=4) + "\n"
    asdf += "\n\n" + ("Cake") + "\n\n"
    for x in Event.objects.all().all_occurrences():
        asdf += pprint.pformat(x, indent=4) + "\n"
    asdf += "</code></pre>"
    return HttpResponse(asdf)

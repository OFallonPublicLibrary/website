from django.contrib import admin
from .models import *

class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('label', 'abbr')


class OccurrenceInline(admin.TabularInline):
    model = Occurrence
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'content')
    list_filter = ('type', )
    search_fields = ('title', 'content')
    inlines = [OccurrenceInline]


admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)

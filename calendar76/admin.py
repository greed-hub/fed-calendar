from django.contrib import admin

# Register your models here.

from .models import Season, Event, Weekly, Daily, EventStyle, CommunityEvent

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ["name",]

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_start', 'date_end', 'event_type',)
    search_fields = ["name", 'date_start', 'date_end', "event_type",]

class CommunityEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_start', 'date_end', 'event_platform',)
    search_fields = ["name", 'date_start', 'date_end', "event_platform",]

class WeeklyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ["name",]

class DailyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ["name",]

class EventStyleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ["name",]

admin.site.register(CommunityEvent, CommunityEventAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Weekly, WeeklyAdmin)
admin.site.register(Daily, DailyAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(EventStyle, EventStyleAdmin)

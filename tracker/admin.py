from django.contrib import admin

# Register your models here.

from .models import Activity, Event

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'is_point', 'is_active')
    list_filter = ['owner']
    search_fields = ['name', 'description']

admin.site.register(Activity, ActivityAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ('activity', 'start_at', 'end_at', 'data')

admin.site.register(Event, EventAdmin)
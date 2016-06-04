from django.contrib import admin

# Register your models here.

from .models import Activity

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_point', 'owner')
    list_filter = ['owner']
    search_fields = ['name', 'description']

admin.site.register(Activity, ActivityAdmin)
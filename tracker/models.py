from django.db import models
from django.conf import settings


class Activity(models.Model):
    class Meta:
        db_table = 'activities'

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_point = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name

class Event(models.Model):
    class Meta:
        db_table = 'events'

    activity = models.ForeignKey(Activity, related_name='events')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    data = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

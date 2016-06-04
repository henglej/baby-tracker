from django.db import models
from django.conf import settings


class Activity(models.Model):
    class Meta:
        db_table = 'activities'

    name = models.CharField(max_length=100)
    description = models.TextField()
    is_point = models.BooleanField(default=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name

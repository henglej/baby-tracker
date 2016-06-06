# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_event_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='activties'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20160605_0230'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='activity',
            field=models.ForeignKey(to='tracker.Activity', related_name='events', default=1),
            preserve_default=False,
        ),
    ]

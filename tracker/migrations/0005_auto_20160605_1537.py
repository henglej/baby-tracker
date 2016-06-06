# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_auto_20160605_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='owner',
            field=models.ForeignKey(related_name='activities', to=settings.AUTH_USER_MODEL),
        ),
    ]

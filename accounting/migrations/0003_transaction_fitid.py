# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20150418_0257'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='fitid',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]

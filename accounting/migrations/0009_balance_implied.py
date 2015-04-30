# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0008_auto_20150421_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='implied',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0011_auto_20150426_2232'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-posted', 'account__name', 'amount']},
        ),
        migrations.AddField(
            model_name='transaction',
            name='display_txt',
            field=models.CharField(default=None, max_length=2000),
            preserve_default=False,
        ),
    ]

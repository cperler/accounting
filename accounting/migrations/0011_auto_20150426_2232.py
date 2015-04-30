# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0010_auto_20150426_1105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['designation', 'type', 'name']},
        ),
        migrations.AlterModelOptions(
            name='balance',
            options={'ordering': ['-as_of_date', 'account__designation', 'account__name', 'amount']},
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['posted', 'account__name', 'amount']},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(unique=True, max_length=150),
            preserve_default=True,
        ),
    ]

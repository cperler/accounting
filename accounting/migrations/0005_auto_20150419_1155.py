# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounting.providers.citi
import accounting.providers.schwab
import accounting.providers.capitalone
import accounting.providers.chase


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_account_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='provider',
            field=models.IntegerField(blank=True, null=True, choices=[(0, accounting.providers.chase.Chase), (1, accounting.providers.capitalone.CapitalOne), (2, accounting.providers.citi.Citibank), (3, accounting.providers.schwab.Schwab)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='fitid',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]

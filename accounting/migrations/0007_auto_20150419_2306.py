# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounting.providers.citi
import accounting.providers.transamerica
import accounting.providers.schwab
import accounting.providers.amex
import accounting.providers.capitalone
import accounting.providers.chase


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0006_account_site_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='provider',
            field=models.IntegerField(blank=True, null=True, choices=[(0, accounting.providers.chase.Chase), (1, accounting.providers.capitalone.CapitalOne), (2, accounting.providers.citi.Citibank), (3, accounting.providers.schwab.Schwab), (4, accounting.providers.amex.AmEx), (5, accounting.providers.citi.Citicard), (6, accounting.providers.transamerica.Transamerica)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
    ]

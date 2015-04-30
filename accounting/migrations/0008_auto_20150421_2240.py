# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounting.providers.citi
import accounting.providers.transamerica
import accounting.providers.schwab
import accounting.providers.amex
import accounting.providers.streetscape
import accounting.providers.capitalone
import accounting.providers.discover
import accounting.providers.nyctrs
import accounting.providers.penn
import accounting.providers.chase


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_auto_20150419_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('as_of_date', models.DateField(db_index=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('account', models.ForeignKey(to='accounting.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='account',
            name='provider',
            field=models.IntegerField(blank=True, null=True, choices=[(0, accounting.providers.chase.Chase), (1, accounting.providers.capitalone.CapitalOne), (2, accounting.providers.citi.Citibank), (3, accounting.providers.schwab.Schwab), (4, accounting.providers.amex.AmEx), (5, accounting.providers.citi.Citicard), (6, accounting.providers.transamerica.Transamerica), (7, accounting.providers.streetscape.Streetscape), (8, accounting.providers.citi.SearsCard), (9, accounting.providers.nyctrs.NYCTrs), (10, accounting.providers.discover.DiscoverStudentLoan), (11, accounting.providers.chase.ChaseMortgage), (12, accounting.providers.penn.PennLifeInsurance)]),
            preserve_default=True,
        ),
    ]

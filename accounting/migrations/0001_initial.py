# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150)),
                ('designation', models.IntegerField(default=0, choices=[(0, b'Assets'), (1, b'Liabilities')])),
                ('url', models.URLField(null=True, blank=True)),
                ('username', models.CharField(max_length=150, null=True, blank=True)),
                ('password', models.CharField(max_length=150, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AccountOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(blank=True, to='accounting.AccountOwner', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='type',
            field=models.ForeignKey(blank=True, to='accounting.AccountType', null=True),
            preserve_default=True,
        ),
    ]

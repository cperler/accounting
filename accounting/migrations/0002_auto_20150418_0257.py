# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounting.providers.capitalone
import accounting.providers.chase


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('regex', models.CharField(max_length=300)),
                ('replacement', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Aliases',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=150)),
                ('category', models.ForeignKey(to='accounting.Category')),
            ],
            options={
                'verbose_name_plural': 'Entities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('posted', models.DateField(db_index=True)),
                ('description', models.CharField(max_length=150)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('check_num', models.PositiveIntegerField(null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(to='accounting.Account')),
                ('entity', models.ForeignKey(to='accounting.Entity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='account',
            name='url',
        ),
        migrations.AddField(
            model_name='account',
            name='download_url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='institute',
            field=models.CharField(default=None, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='login_url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='number',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='provider',
            field=models.IntegerField(blank=True, null=True, choices=[(0, accounting.providers.chase.Chase), (1, accounting.providers.capitalone.CapitalOne)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(help_text=b'Will auto-populate if blank upon saving.', unique=True, max_length=150, blank=True),
            preserve_default=True,
        ),
    ]

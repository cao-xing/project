# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pj01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('email', models.CharField(default='', max_length=32)),
                ('phone', models.CharField(default='', max_length=32)),
            ],
        ),
    ]

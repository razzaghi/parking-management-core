# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-03-08 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nad_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkinginout',
            name='exited',
            field=models.BooleanField(default=False),
        ),
    ]
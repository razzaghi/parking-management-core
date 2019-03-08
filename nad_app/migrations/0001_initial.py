# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-03-08 09:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import nad_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerInvoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reserveType', enumfields.fields.EnumField(enum=nad_app.models.ReserveType, max_length=1)),
                ('state', enumfields.fields.EnumField(enum=nad_app.models.State, max_length=1)),
                ('entrancePrice', models.FloatField(default=0, verbose_name=b'EntrancePrice')),
                ('priceForEachHour', models.FloatField(default=0, verbose_name=b'PriceForEachHour')),
                ('priceForEachDay', models.FloatField(default=0, verbose_name=b'PriceForEachDay')),
                ('carNumber', models.CharField(max_length=255, verbose_name=b'carNumber')),
                ('startDateTime', models.DateTimeField(auto_now_add=True)),
                ('finishDateTime', models.DateTimeField()),
                ('totalHours', models.FloatField(default=0, verbose_name=b'TotalHours')),
                ('totalDays', models.FloatField(default=0, verbose_name=b'TotalDays')),
                ('totalPrice', models.FloatField(default=0, verbose_name=b'TotalPrice')),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('capacity', models.IntegerField(default=50, verbose_name=b'Capacity')),
                ('entrancePrice', models.FloatField(default=0, verbose_name=b'EntrancePrice')),
                ('priceForEachHour', models.FloatField(default=0, verbose_name=b'PriceForEachHour')),
                ('priceForEachDay', models.FloatField(default=0, verbose_name=b'PriceForEachDay')),
                ('isDaily', models.BooleanField(default=True)),
                ('availableSpace', models.IntegerField(default=50, verbose_name=b'AvailableSpace')),
            ],
        ),
        migrations.CreateModel(
            name='ParkingInOut',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reserveType', enumfields.fields.EnumField(enum=nad_app.models.ReserveType, max_length=1)),
                ('state', enumfields.fields.EnumField(enum=nad_app.models.State, max_length=1)),
                ('carNumber', models.CharField(max_length=255, verbose_name=b'carNumber')),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('parking', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='nad_app.Parking', verbose_name=b'Parking')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'User')),
            ],
        ),
        migrations.CreateModel(
            name='ParkingType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ReserveStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('isAvailable', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='parking',
            name='type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='nad_app.ParkingType', verbose_name=b'ParkingType'),
        ),
        migrations.AddField(
            model_name='customerinvoice',
            name='parking',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='nad_app.Parking', verbose_name=b'Parking'),
        ),
        migrations.AddField(
            model_name='customerinvoice',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'User'),
        ),
    ]
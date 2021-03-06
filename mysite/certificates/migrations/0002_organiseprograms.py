# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 05:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certificates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisePrograms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('num_of_days', models.IntegerField()),
                ('days_attended', models.IntegerField()),
                ('qrCode', models.IntegerField()),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificates.Programs')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

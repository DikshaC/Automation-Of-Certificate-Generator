# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 22:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certificates', '0021_auto_20170530_1217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisedevent',
            name='participant',
        ),
        migrations.AddField(
            model_name='organisedevent',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]

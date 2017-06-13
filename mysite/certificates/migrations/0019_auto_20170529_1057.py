# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-29 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0018_merge_20170529_1049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organisedevent',
            old_name='program',
            new_name='event',
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='latex_template',
        ),
        migrations.AddField(
            model_name='certificate',
            name='template',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

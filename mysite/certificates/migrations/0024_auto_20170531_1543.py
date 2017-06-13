# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 22:43
from __future__ import unicode_literals

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0023_auto_20170531_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='template',
            field=models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(), upload_to='media'),
        ),
        migrations.AlterField(
            model_name='event',
            name='creator',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='organisedevent',
            name='organiser',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='organisedevent',
            name='participants',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='organisedevent',
            name='place',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='college',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='usertype',
            name='user',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]

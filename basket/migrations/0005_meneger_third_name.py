# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-11 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0004_auto_20181011_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='meneger',
            name='third_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
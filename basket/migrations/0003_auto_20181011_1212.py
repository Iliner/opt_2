# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-11 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0002_meneger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meneger',
            name='customers',
            field=models.ManyToManyField(to='basket.Customer'),
        ),
    ]
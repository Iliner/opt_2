# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-26 09:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0004_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='basket.Customer'),
        ),
    ]
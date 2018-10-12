# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-11 09:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meneger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('mail_own', models.EmailField(blank=True, max_length=254, null=True)),
                ('mail_work', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number_own', models.CharField(blank=True, max_length=30, null=True)),
                ('phone_number_work', models.CharField(blank=True, max_length=30, null=True)),
                ('customers', models.ManyToManyField(blank=True, null=True, to='basket.Customer')),
            ],
            options={
                'verbose_name': 'Менеджер',
                'verbose_name_plural': 'Менеджеры',
            },
        ),
    ]

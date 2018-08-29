# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-16 10:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0002_auto_20180809_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('photo_width', models.IntegerField(default=0)),
                ('photo_height', models.IntegerField(default=0)),
                ('photo', models.ImageField(upload_to='')),
                ('code', models.IntegerField()),
                ('image_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Изображение',
                'ordering': ['date'],
            },
        ),
        migrations.AddField(
            model_name='goods',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_page.Photo'),
        ),
    ]

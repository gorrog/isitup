# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 01:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='url',
            field=models.CharField(max_length=500),
        ),
    ]
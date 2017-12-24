# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-22 11:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_heart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heart',
            name='lover',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
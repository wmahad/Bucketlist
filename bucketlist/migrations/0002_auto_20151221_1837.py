# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 18:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketlistitem',
            name='bucketlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='bucketlist.BucketList'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_wallpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_userprofile_friends_+', to='person.UserProfile'),
        ),
    ]

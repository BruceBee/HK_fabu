# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='create_time',
            field=models.CharField(default=b'0000-00-00 00:00:00', max_length=20),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='update_time',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='update_user',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_status',
            field=models.CharField(default=b'1', max_length=2),
        ),
    ]

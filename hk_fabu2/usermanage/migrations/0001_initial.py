# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user', models.CharField(max_length=16, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=32)),
                ('ftp_path', models.CharField(max_length=32)),
                ('remark', models.CharField(max_length=32)),
                ('have_publish', models.CharField(default=b'1', max_length=4)),
                ('have_review', models.CharField(default=b'1', max_length=4)),
                ('have_test', models.CharField(default=b'1', max_length=4)),
            ],
        ),
    ]

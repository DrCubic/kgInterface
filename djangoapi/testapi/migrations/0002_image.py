# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Iname', models.CharField(max_length=32, null=True, blank=True)),
                ('Iid', models.CharField(unique=True, max_length=32, db_index=True)),
                ('Fid', models.CharField(unique=True, max_length=32, db_index=True)),
            ],
        ),
    ]

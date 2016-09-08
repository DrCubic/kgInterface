# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapi', '0003_auto_20160318_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medication',
            name='Ejfl',
        ),
        migrations.RemoveField(
            model_name='medication',
            name='Sjfl',
        ),
        migrations.RemoveField(
            model_name='medication',
            name='Yjfl',
        ),
        migrations.RemoveField(
            model_name='medication',
            name='Ywbm',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapi', '0002_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lab',
            name='Ejfl',
        ),
        migrations.RemoveField(
            model_name='lab',
            name='Yjfl',
        ),
        migrations.AlterField(
            model_name='lab',
            name='Name',
            field=models.CharField(max_length=64, db_index=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Blfy',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Ejfl',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Ename',
            field=models.CharField(db_index=True, max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Fclass',
            field=models.CharField(db_index=True, max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Jjz',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Name',
            field=models.CharField(max_length=128, db_index=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Oname',
            field=models.CharField(db_index=True, max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Sclass',
            field=models.CharField(db_index=True, max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Sjfl',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Syz',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Tclass',
            field=models.CharField(db_index=True, max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Ydx',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Yfyl',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Yjfl',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Ylzy',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Ywbm',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Ywjx',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Ywxyzy',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Zjdp',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='Zysx',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
    ]

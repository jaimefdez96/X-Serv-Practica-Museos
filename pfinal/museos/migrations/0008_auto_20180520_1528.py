# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0007_auto_20180520_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 20, 15, 28, 48, 366084, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='conf',
            name='fuente',
            field=models.CharField(default='10px', max_length=32),
        ),
        migrations.AlterField(
            model_name='selec',
            name='fecha',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 20, 15, 28, 48, 363938, tzinfo=utc)),
        ),
    ]

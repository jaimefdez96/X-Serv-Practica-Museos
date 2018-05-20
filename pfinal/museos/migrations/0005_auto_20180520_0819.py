# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0004_auto_20180519_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 20, 8, 19, 56, 362413, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='conf',
            name='color',
            field=models.CharField(max_length=32, default='gainsboro'),
        ),
        migrations.AlterField(
            model_name='conf',
            name='fuente',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='conf',
            name='titulo',
            field=models.CharField(max_length=32, default=''),
        ),
        migrations.AlterField(
            model_name='selec',
            name='fecha',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 20, 8, 19, 56, 360193, tzinfo=utc)),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0009_auto_20180520_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 20, 22, 10, 28, 279562, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='conf',
            name='fuente',
            field=models.CharField(max_length=3, default='18px'),
        ),
        migrations.AlterField(
            model_name='selec',
            name='fecha',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 20, 22, 10, 28, 277420, tzinfo=utc)),
        ),
    ]

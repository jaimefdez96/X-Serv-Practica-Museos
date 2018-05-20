# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0008_auto_20180520_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 20, 18, 54, 43, 923392, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='conf',
            name='fuente',
            field=models.CharField(max_length=3, default='20px'),
        ),
        migrations.AlterField(
            model_name='selec',
            name='fecha',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 20, 18, 54, 43, 920522, tzinfo=utc)),
        ),
    ]

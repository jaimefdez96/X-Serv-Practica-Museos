# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0010_auto_20180520_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 20, 22, 11, 45, 874062, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='conf',
            name='fuente',
            field=models.CharField(max_length=3, default='15px'),
        ),
        migrations.AlterField(
            model_name='selec',
            name='fecha',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 20, 22, 11, 45, 871901, tzinfo=utc)),
        ),
    ]

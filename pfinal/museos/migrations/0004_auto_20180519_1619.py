# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0003_auto_20180519_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 19, 16, 19, 15, 446442, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='selec',
            name='fecha',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 19, 16, 19, 15, 444078, tzinfo=utc)),
        ),
    ]

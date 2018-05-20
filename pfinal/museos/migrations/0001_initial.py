# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('autor', models.CharField(max_length=32)),
                ('texto', models.TextField()),
                ('fecha', models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 19, 16, 2, 47, 437243, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='Conf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('titulo', models.CharField(max_length=32)),
                ('color', models.CharField(max_length=32)),
                ('fuente', models.PositiveIntegerField()),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=32)),
                ('descripcion', models.TextField()),
                ('horario', models.TextField()),
                ('transporte', models.TextField()),
                ('accesibilidad', models.BooleanField(default=False)),
                ('url', models.TextField()),
                ('calle', models.CharField(max_length=32)),
                ('numero', models.CharField(max_length=32)),
                ('localidad', models.CharField(max_length=32)),
                ('codigo_postal', models.CharField(max_length=32)),
                ('distrito', models.CharField(max_length=32)),
                ('telefono', models.CharField(max_length=32)),
                ('fax', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Selec',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha', models.DateTimeField(verbose_name=datetime.datetime(2018, 5, 19, 16, 2, 47, 434936, tzinfo=utc))),
                ('museo', models.ManyToManyField(to='museos.Museo')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comentario',
            name='museo',
            field=models.ForeignKey(to='museos.Museo'),
        ),
    ]

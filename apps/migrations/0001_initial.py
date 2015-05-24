# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('tipo', models.CharField(max_length=100)),
                ('precio', models.CharField(max_length=32)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('duracion', models.DateTimeField()),
                ('eslargo', models.IntegerField()),
                ('urlinfo', models.TextField()),
                ('fechamod', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Actividad_User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('urlinfo', models.TextField()),
                ('fechaadd', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=32)),
                ('descripcion', models.TextField()),
                ('actividades', models.ManyToManyField(to='apps.Actividad_User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

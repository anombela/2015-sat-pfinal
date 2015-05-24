# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tituloactividad', models.CharField(max_length=100)),
                ('comentario', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=32)),
                ('titulo', models.CharField(max_length=100)),
                ('comments', models.ManyToManyField(to='apps.Comentario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Variablescss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=100)),
                ('colorletra', models.CharField(default=b'', max_length=32)),
                ('tamannoletra', models.CharField(default=b'', max_length=32)),
                ('colorfondo', models.CharField(default=b'', max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='actividad',
            name='masinfo',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='actividad',
            name='puntuacion',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actividad_user',
            name='comentario',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='css',
            field=models.ManyToManyField(to='apps.Variablescss'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='title',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]

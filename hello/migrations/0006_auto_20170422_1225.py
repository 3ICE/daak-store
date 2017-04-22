# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-22 09:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hello', '0005_player_activated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, db_tablespace=None, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(db_tablespace=None, default=0)),
                ('state', models.TextField(blank=True, db_tablespace=None, null=True)),
                ('game', models.ForeignKey(db_tablespace=None, on_delete=django.db.models.deletion.CASCADE, to='hello.Game')),
                ('player', models.ForeignKey(db_tablespace=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='scores',
            name='game',
        ),
        migrations.RemoveField(
            model_name='scores',
            name='player',
        ),
        migrations.DeleteModel(
            name='Scores',
        ),
    ]
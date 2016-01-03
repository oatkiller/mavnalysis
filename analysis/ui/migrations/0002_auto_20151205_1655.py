# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('exerciseName', models.CharField(max_length=100, null=True, blank=True)),
                ('reps', models.SmallIntegerField()),
                ('weight', models.DecimalField(max_digits=14, decimal_places=2)),
                ('isBodyWeight', models.BooleanField(default=False)),
                ('isLbs', models.BooleanField(default=False)),
                ('isPR', models.BooleanField(default=False)),
                ('isSeconds', models.BooleanField(default=False)),
                ('hasFailure', models.BooleanField(default=False)),
                ('extras', models.CharField(max_length=500, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('set', models.ForeignKey(blank=True, to='ui.ExerciseSet', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('workout_text', models.CharField(max_length=19000, null=True, blank=True)),
                ('has_pr', models.BooleanField(default=False)),
                ('comments', models.CharField(default='', max_length=10000)),
            ],
        ),
        migrations.AddField(
            model_name='exerciseset',
            name='workout',
            field=models.ForeignKey(related_name='sets', to='ui.Workout', null=True),
        ),
    ]

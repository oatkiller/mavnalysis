# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from ui.models import *
from analysis import WorkoutLogParser


def create_workouts(apps, schema_editor):
	try:
		Posts.objects.all()
	except Exception:
		return
	for post in Posts.objects.all():
		w = Workout(date=post.post_date, workout_text=post.post_content)
		print('saving new workout...')
		w.save()

def delete_workouts(apps, schema_editor):
	Workout.objects.all().delete()

def create_sets(apps, schema_editor):
	for workout in Workout.objects.all():
		parser = WorkoutLogParser(workout)
		parser.parse()

def delete_sets(apps, schema_editor):
	ExerciseSet.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0002_auto_20151117_2113'),
    ]

    operations = [
		#	migrations.RunPython(create_workouts,delete_workouts),
		 #	migrations.RunPython(create_sets, delete_sets)
    ]

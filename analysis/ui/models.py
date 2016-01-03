# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



class Posts(models.Model):
    post_author = models.BigIntegerField(blank=True, null=True)
    post_date = models.DateTimeField(blank=True, null=True)
    post_date_gmt = models.DateTimeField(blank=True, null=True)
    post_content = models.CharField(max_length=19000, blank=True, null=True)
    post_title = models.CharField(max_length=300, blank=True, null=True)
    post_excerpt = models.CharField(max_length=9000, blank=True, null=True)
    post_status = models.CharField(max_length=20, blank=True, null=True)
    comment_status = models.CharField(max_length=20, blank=True, null=True)
    ping_status = models.CharField(max_length=20, blank=True, null=True)
    post_password = models.CharField(max_length=20, blank=True, null=True)
    post_name = models.CharField(max_length=200, blank=True, null=True)
    to_ping = models.CharField(max_length=700, blank=True, null=True)
    pinged = models.CharField(max_length=700, blank=True, null=True)
    post_modified = models.DateTimeField(blank=True, null=True)
    post_modified_gmt = models.DateTimeField(blank=True, null=True)
    post_content_filtered = models.CharField(max_length=400, blank=True, null=True)
    post_parent = models.BigIntegerField(blank=True, null=True)
    guid = models.CharField(max_length=255, blank=True, null=True)
    menu_order = models.SmallIntegerField(blank=True, null=True)
    post_type = models.CharField(max_length=20, blank=True, null=True)
    post_mime_type = models.CharField(max_length=100, blank=True, null=True)
    comment_count = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'

class Workout(models.Model):
	date = models.DateTimeField(blank=True, null=True)
	workout_text = models.CharField(max_length=19000, blank=True, null=True)
	has_pr = models.BooleanField(default=False)	
	comments = models.CharField(max_length=10000, default="")

class ExerciseSet(models.Model):
	date = models.DateTimeField(blank=True, null=True)
	user = models.ForeignKey(User, blank=False, null=True)
	exerciseName = models.CharField(max_length=100, blank=True, null=True)
	reps = models.SmallIntegerField()
	weight = models.DecimalField(max_digits=14, decimal_places=2)
	isBodyWeight = models.BooleanField(default=False)
	isLbs = models.BooleanField(default=False)
	isPR = models.BooleanField(default=False)
	isSeconds = models.BooleanField(default=False)
	hasFailure = models.BooleanField(default=False)
	workout = models.ForeignKey(Workout, null=True, related_name="sets") 
	extras = models.CharField(max_length=500, blank=True, null=True)

class PersonalRecord(models.Model):
	set = models.ForeignKey(ExerciseSet, blank=True, null=True)
	user = models.ForeignKey(User, blank=False, null=True)

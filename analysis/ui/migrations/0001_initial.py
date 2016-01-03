# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_author', models.BigIntegerField(null=True, blank=True)),
                ('post_date', models.DateTimeField(null=True, blank=True)),
                ('post_date_gmt', models.DateTimeField(null=True, blank=True)),
                ('post_content', models.CharField(max_length=19000, null=True, blank=True)),
                ('post_title', models.CharField(max_length=300, null=True, blank=True)),
                ('post_excerpt', models.CharField(max_length=9000, null=True, blank=True)),
                ('post_status', models.CharField(max_length=20, null=True, blank=True)),
                ('comment_status', models.CharField(max_length=20, null=True, blank=True)),
                ('ping_status', models.CharField(max_length=20, null=True, blank=True)),
                ('post_password', models.CharField(max_length=20, null=True, blank=True)),
                ('post_name', models.CharField(max_length=200, null=True, blank=True)),
                ('to_ping', models.CharField(max_length=700, null=True, blank=True)),
                ('pinged', models.CharField(max_length=700, null=True, blank=True)),
                ('post_modified', models.DateTimeField(null=True, blank=True)),
                ('post_modified_gmt', models.DateTimeField(null=True, blank=True)),
                ('post_content_filtered', models.CharField(max_length=400, null=True, blank=True)),
                ('post_parent', models.BigIntegerField(null=True, blank=True)),
                ('guid', models.CharField(max_length=255, null=True, blank=True)),
                ('menu_order', models.SmallIntegerField(null=True, blank=True)),
                ('post_type', models.CharField(max_length=20, null=True, blank=True)),
                ('post_mime_type', models.CharField(max_length=100, null=True, blank=True)),
                ('comment_count', models.BigIntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'posts',
                'managed': False,
            },
        ),
    ]

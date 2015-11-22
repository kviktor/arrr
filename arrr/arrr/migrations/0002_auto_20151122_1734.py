# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('arrr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='changed_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('p', 'pending'), ('r', 'rejected'), ('a', 'approved')], max_length=1, default='p'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='title',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, always_update=True, unique=True, populate_from='name'),
        ),
    ]

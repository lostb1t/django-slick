# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slick', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='actionnotify',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='actionnotify',
            name='action',
        ),
        migrations.RemoveField(
            model_name='actionnotify',
            name='user',
        ),
        migrations.DeleteModel(
            name='ActionNotify',
        ),
    ]

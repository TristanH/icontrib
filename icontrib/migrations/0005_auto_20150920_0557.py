# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icontrib', '0004_auto_20150920_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='twitter_post_id',
            field=models.CharField(max_length=256, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icontrib', '0003_auto_20150919_2206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contribution',
            old_name='twitter_post_link',
            new_name='twitter_post_id',
        ),
    ]

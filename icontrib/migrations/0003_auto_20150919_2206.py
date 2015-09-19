# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icontrib', '0002_userprofile_braintree_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='hashtag',
            field=models.CharField(unique=True, max_length=24),
        ),
    ]

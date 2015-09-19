# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icontrib', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='braintree_customer_id',
            field=models.CharField(default=b'null', max_length=128),
        ),
    ]

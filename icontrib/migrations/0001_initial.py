# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hashtag', models.CharField(max_length=24)),
                ('target_amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('contribution_amount', models.DecimalField(default=1.0, max_digits=6, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('twitter_post_link', models.CharField(max_length=256)),
                ('confirmed', models.BooleanField(default=False)),
                ('campaign', models.ForeignKey(to='icontrib.Campaign')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='contribution',
            name='profile',
            field=models.ForeignKey(to='icontrib.UserProfile'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='organizer_profile',
            field=models.ForeignKey(to='icontrib.UserProfile'),
        ),
    ]

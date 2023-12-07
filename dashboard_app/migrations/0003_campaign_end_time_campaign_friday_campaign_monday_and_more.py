# Generated by Django 4.2.5 on 2023-11-29 08:52

import datetime
from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0002_rename_name_campaign_campaign_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='end_time',
            field=models.TimeField(default=datetime.time(17, 0)),
        ),
        migrations.AddField(
            model_name='campaign',
            name='friday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campaign',
            name='monday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campaign',
            name='saturday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campaign',
            name='start_time',
            field=models.TimeField(default=datetime.time(9, 0)),
        ),
        migrations.AddField(
            model_name='campaign',
            name='sunday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campaign',
            name='thursday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campaign',
            name='tuesday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campaign',
            name='wednesday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(),
        ),
    ]
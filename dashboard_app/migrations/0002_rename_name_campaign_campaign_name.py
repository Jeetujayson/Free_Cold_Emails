# Generated by Django 4.2.5 on 2023-11-27 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='name',
            new_name='campaign_name',
        ),
    ]

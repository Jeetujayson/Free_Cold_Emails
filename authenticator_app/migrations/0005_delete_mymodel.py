# Generated by Django 4.2.5 on 2023-10-06 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator_app', '0004_mymodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyModel',
        ),
    ]
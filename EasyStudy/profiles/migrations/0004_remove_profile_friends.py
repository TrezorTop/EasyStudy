# Generated by Django 3.0.5 on 2021-04-23 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_relationship'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='friends',
        ),
    ]

# Generated by Django 3.0.5 on 2021-05-01 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20210501_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, to='profiles.Profile'),
        ),
    ]
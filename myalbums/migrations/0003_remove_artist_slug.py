# Generated by Django 3.0.8 on 2020-08-30 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myalbums', '0002_artist_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='slug',
        ),
    ]
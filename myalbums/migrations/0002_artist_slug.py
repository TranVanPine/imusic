# Generated by Django 3.0.8 on 2020-08-30 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myalbums', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='slug',
            field=models.SlugField(max_length=40, null=True),
        ),
    ]

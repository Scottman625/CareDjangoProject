# Generated by Django 4.0.5 on 2022-09-12 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0037_message_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userweekdaytime',
            name='end_time',
            field=models.FloatField(blank=True, default=24, null=True),
        ),
        migrations.AddField(
            model_name='userweekdaytime',
            name='sstart_time',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]

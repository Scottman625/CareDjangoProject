# Generated by Django 4.0.5 on 2022-09-10 13:37

from django.db import migrations, models
import modelCore.models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0036_alter_userweekdaytime_end_time_hour_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=modelCore.models.image_upload_handler),
        ),
    ]

# Generated by Django 4.0.5 on 2022-09-01 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0020_merge_20220901_0140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='license',
            name='isPassed',
        ),
        migrations.AddField(
            model_name='userlicenseshipimage',
            name='isPassed',
            field=models.BooleanField(default=False),
        ),
    ]

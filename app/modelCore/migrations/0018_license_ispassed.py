# Generated by Django 4.0.5 on 2022-08-31 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0017_merge_20220831_0216'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='isPassed',
            field=models.BooleanField(default=False),
        ),
    ]

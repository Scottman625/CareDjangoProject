# Generated by Django 4.0.5 on 2022-06-19 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0005_alter_recipient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
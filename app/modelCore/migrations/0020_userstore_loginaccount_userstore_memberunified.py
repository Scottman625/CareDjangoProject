# Generated by Django 4.0.5 on 2022-10-04 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0019_county_addresscode'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstore',
            name='LoginAccount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userstore',
            name='MemberUnified',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

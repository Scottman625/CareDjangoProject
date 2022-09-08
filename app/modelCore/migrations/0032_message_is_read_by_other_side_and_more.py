# Generated by Django 4.0.5 on 2022-09-08 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0031_alter_userserviceship_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read_by_other_side',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='refound_apply_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='refound_money',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]

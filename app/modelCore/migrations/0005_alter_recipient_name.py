# Generated by Django 4.0.5 on 2022-06-19 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0004_alter_category_care_type_alter_category_time_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
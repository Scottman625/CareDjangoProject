# Generated by Django 4.0.5 on 2022-06-19 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0003_caseserviceitemship_markupitem_orderserviceitemship_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='care_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='time_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
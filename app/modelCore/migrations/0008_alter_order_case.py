# Generated by Django 4.0.5 on 2022-06-19 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0007_orderstate_remove_case_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='case',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modelCore.case'),
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-29 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0004_case_care_type_case_is_alltime_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='servant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cases', to='modelCore.servant'),
        ),
        migrations.AlterField(
            model_name='case',
            name='specify_servant_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cases_specify_1', to='modelCore.servant'),
        ),
        migrations.AlterField(
            model_name='case',
            name='specify_servant_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cases_specify_2', to='modelCore.servant'),
        ),
        migrations.AlterField(
            model_name='case',
            name='specify_servant_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cases_specify_3', to='modelCore.servant'),
        ),
        migrations.AlterField(
            model_name='servantweekdaytime',
            name='servant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='weekdayTimes', to='modelCore.servant'),
        ),
        migrations.AlterField(
            model_name='transportation',
            name='servant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='transportations', to='modelCore.servant'),
        ),
    ]

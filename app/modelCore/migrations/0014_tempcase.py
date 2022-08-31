# Generated by Django 4.0.5 on 2022-08-30 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0013_blogcategory_blogpost_blogpostcategoryship'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('care_type', models.CharField(choices=[('home', '居家照顧'), ('hospital', '醫院看護')], default='', max_length=10)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('state', models.CharField(choices=[('unTaken', '未承接'), ('unComplete', '未完成'), ('Complete', '已完成'), ('Canceled', '取消'), ('endEarly', '提早結束')], default='unTaken', max_length=10)),
                ('age', models.IntegerField(blank=True, default=0, null=True)),
                ('weight', models.IntegerField(blank=True, default=0, null=True)),
                ('disease_remark', models.CharField(blank=True, max_length=255, null=True)),
                ('conditions_remark', models.CharField(blank=True, max_length=255, null=True)),
                ('is_continuous_time', models.BooleanField(default=False)),
                ('is_taken', models.BooleanField(default=False)),
                ('is_open_for_search', models.BooleanField(default=False)),
                ('body_condition', models.CharField(blank=True, max_length=255, null=True)),
                ('disease', models.CharField(blank=True, max_length=255, null=True)),
                ('service', models.CharField(blank=True, max_length=255, null=True)),
                ('weekday', models.CharField(blank=True, max_length=100, null=True)),
                ('start_time', models.FloatField(blank=True, default=0, null=True)),
                ('end_time', models.FloatField(blank=True, default=24, null=True)),
                ('start_datetime', models.DateTimeField(blank=True, null=True)),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('emergencycontact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('emergencycontact_relation', models.CharField(blank=True, max_length=100, null=True)),
                ('emergencycontact_phone', models.CharField(blank=True, max_length=10, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='modelCore.city')),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.county')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 4.0.1 on 2022-06-19 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0002_bodyconditions_case_category_city_cityarea_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseServiceItemShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MarkupItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderServiceItemShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ServantMarkupItemPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('markup_item', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.markupitem')),
                ('servant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.servant')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('info', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='servantmarkupitemship',
            name='markup_item',
        ),
        migrations.RemoveField(
            model_name='servantmarkupitemship',
            name='servant',
        ),
        migrations.RemoveField(
            model_name='case',
            name='service_items',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='info',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='transportation',
            name='price',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='line_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='conditions',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='BodyConditions',
        ),
        migrations.DeleteModel(
            name='MarkupItems',
        ),
        migrations.DeleteModel(
            name='ServantMarkupItemShip',
        ),
        migrations.AddField(
            model_name='orderserviceitemship',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.order'),
        ),
        migrations.AddField(
            model_name='orderserviceitemship',
            name='service_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.serviceitem'),
        ),
        migrations.AddField(
            model_name='caseserviceitemship',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.case'),
        ),
        migrations.AddField(
            model_name='caseserviceitemship',
            name='service_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.serviceitem'),
        ),
        migrations.AlterField(
            model_name='order',
            name='service_items',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.serviceitem'),
        ),
        migrations.DeleteModel(
            name='ServiceItems',
        ),
    ]
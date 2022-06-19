# Generated by Django 4.0.5 on 2022-06-19 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0006_alter_case_end_date_alter_case_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='case',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='service_items',
        ),
        migrations.RemoveField(
            model_name='payinfo',
            name='case',
        ),
        migrations.AddField(
            model_name='case',
            name='recipient',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to='modelCore.recipient'),
        ),
        migrations.AddField(
            model_name='payinfo',
            name='order',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to='modelCore.order'),
        ),
        migrations.AlterField(
            model_name='orderreview',
            name='customer_review_createdate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderreview',
            name='servant_review_createdate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='modelCore.orderstate'),
        ),
    ]

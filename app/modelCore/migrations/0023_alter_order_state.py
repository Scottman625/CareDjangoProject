# Generated by Django 4.0.5 on 2022-07-13 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0022_alter_review_case_offender_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(choices=[('unPaid', '未付款'), ('paid', '已付款'), ('canceled', '已取消')], default='unPaid', max_length=10),
        ),
    ]

# Generated by Django 4.0.5 on 2022-09-15 04:06

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0041_alter_userlicenseshipimage_license'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssistancePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('body', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
        ),
    ]

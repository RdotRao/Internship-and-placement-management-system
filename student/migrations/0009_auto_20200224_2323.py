# Generated by Django 3.0 on 2020-02-24 23:23

from django.db import migrations, models
import student.models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20200224_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to=student.models.content_file_name_photo),
        ),
        migrations.AlterField(
            model_name='details',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to=student.models.content_file_name),
        ),
        migrations.AlterField(
            model_name='details',
            name='sign',
            field=models.FileField(blank=True, null=True, upload_to=student.models.content_file_name_sign),
        ),
    ]
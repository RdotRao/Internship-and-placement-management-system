# Generated by Django 3.0 on 2020-02-27 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_delete_date_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='applied',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

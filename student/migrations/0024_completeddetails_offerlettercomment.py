# Generated by Django 3.0 on 2020-04-12 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0023_auto_20200412_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='completeddetails',
            name='OfferLetterComment',
            field=models.TextField(blank=True, null=True),
        ),
    ]

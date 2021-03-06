# Generated by Django 3.0 on 2020-04-11 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0020_auto_20200410_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='completeddetails',
            name='NOCDetails',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='completeddetails',
            name='NOCgenerated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='completeddetails',
            name='OfferLetter',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='completeddetails',
            name='OfferLetterNotSubmitted',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 3.0 on 2020-03-13 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunity', '0008_results_results_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
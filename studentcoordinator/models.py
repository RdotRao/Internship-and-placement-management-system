from django.db import models

class city(models.Model):
    city_name = models.CharField(blank=True,null=True,max_length=30)
from django.db import models

from django.urls import reverse
# Create your models here.

class fdetails(models.Model):
    Gender=(

        ('G','Male'),
        ('G','Female'),
        ('G','Other'),
    )
    empcode = models.TextField(primary_key=True)#max len 6
    name = models.TextField()
    middlename = models.TextField()
    lastname = models.TextField()
    email = models.EmailField(blank=True)
    phno = models.TextField()
    gender = models.TextField(choices=Gender)
    

from __future__ import unicode_literals
from django.db import models
import os 
from django.urls import reverse
import hashlib


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    name = 'A'+str(instance.enrollmentno)+'Z'
    name = encrypt_string(name)
    filename = "%s.%s" % (name, ext)
    return os.path.join('documents/', filename)

def content_file_name_photo(instance, filename):
    ext = filename.split('.')[-1]
    name = 'Z'+str(instance.enrollmentno)+'A'
    name = encrypt_string(name)
    filename = "%s.%s" % (name, ext)
    return os.path.join('userphotos/', filename)

def content_file_name_sign(instance, filename):
    ext = filename.split('.')[-1]
    name = 'S'+str(instance.enrollmentno)+'N'
    name = encrypt_string(name)
    filename = "%s.%s" % (name, ext)
    return os.path.join('usersign/', filename)


class applied(models.Model):
    encode_company = models.CharField(blank=True,null=True,max_length=100)
    enrollmentno = models.CharField(blank=True,null=True,max_length=11)
    name = models.CharField(blank=True,null=True,max_length=100)
    
class position(models.Model):
    name = models.TextField()

class completeddetails(models.Model):
    enrollmentno = models.CharField(primary_key=True,max_length=11)
    filleddetails = models.BooleanField(default=False)
    internship = models.BooleanField(default=False)
    placement = models.BooleanField(default=False)
    placementselected = models.BooleanField(default=False)
    internshipselected = models.BooleanField(default=False)
    NOCgenerated = models.BooleanField(default=False)
    OfferLetterNotSubmitted = models.BooleanField(default=True)
    NOCDetails = models.FileField(blank=True,null=True)
    OfferLetter =  models.FileField(blank=True,null=True)
    OfferLetterVerified = models.BooleanField(default=False)
    OfferLetterComment = models.TextField(blank=True, null=True)
    
class details(models.Model):
    Specialization=(
        ('BTECH-CSE-BDA','BTECH-CSE-BDA'),
        ('BTECH-CSE-CBA','BTECH-CSE-CBA'),
        ('BTECH-CSE-CS','BTECH-CSE-CS'),
    )
    Gender=(

        ('M','Male'),
        ('G','Female'),
        ('O','Other'),
    )
    sscboard = (
        ('GSEB','GSEB'),
        ('CBSE','CBSE'),
        ('ICSE','ICSE'),
        ('OTHER','OTHER'),
        )

    hscboard = (
        ('GSHEB','GSHEB'),
        ('CBSE','CBSE'),
        ('ICSE','ICSE'),
        ('OTHER','OTHER'),
        )
    enrollmentno = models.CharField(primary_key=True,max_length=11)
    firstname = models.CharField(blank=True,null=True,max_length=30)
    middlename = models.CharField(blank=True, null=True,max_length=30)
    lastname = models.CharField(blank=True, null=True,max_length=30)
    gender = models.CharField(blank=True, null=True,choices=Gender,max_length=30)
    dob = models.DateField(blank=True,null=True)
    phno = models.CharField(max_length=10,blank=True, null=True)
    parentphno = models.CharField(max_length=10,blank=True, null=True)
    program = models.TextField(choices=Specialization,max_length=30,blank=True,null=True)
    email = models.EmailField(blank=True, null=True)
    ssc_year = models.PositiveSmallIntegerField(blank=True, null=True)
    ssc_percentage = models.FloatField(blank=True, null=True)
    ssc_board = models.TextField(choices=sscboard,blank=True, null=True)
    hsc_year = models.PositiveSmallIntegerField(blank=True, null=True)
    hsc_percentage = models.FloatField(blank=True, null=True)
    hsc_board = models.CharField(choices=hscboard,blank=True, null=True,max_length=30)
    diploma_year = models.PositiveSmallIntegerField(blank=True, null=True)
    diploma_university = models.CharField(blank=True, null=True,max_length=30)
    diploma_percentage = models.FloatField(blank=True, null=True)
    sgpa_sem_1 =  models.FloatField(blank=True, null=True)
    sgpa_sem_2 =  models.FloatField(blank=True, null=True)
    sgpa_sem_3 =  models.FloatField(blank=True, null=True)
    sgpa_sem_4 =  models.FloatField(blank=True, null=True)
    sgpa_sem_5 =  models.FloatField(blank=True, null=True)
    sgpa_sem_6 =  models.FloatField(blank=True, null=True)
    sgpa_sem_7 =  models.FloatField(blank=True, null=True)
    sgpa_sem_8 =  models.FloatField(blank=True, null=True)
    cgpa =  models.FloatField(blank=True, null=True)
    cityofinterest =  models.TextField(blank=True, null=True)
    skillset = models.TextField(blank=True, null=True)
    positionofinterest = models.TextField(blank=True, null=True)
    toolsandtechnology = models.TextField(blank=True, null=True)
    linkedinURL = models.URLField(max_length=400,blank=True,null=True)
    effbacklog = models.PositiveSmallIntegerField(blank=True, null=True)
    resume = models.FileField(upload_to=content_file_name,blank=True,null=True)
    photo = models.FileField(upload_to=content_file_name_photo,blank=True,null=True)
    sign = models.FileField(upload_to=content_file_name_sign,blank=True,null=True)
	
class placed(models.Model):
    enrollmentno = models.OneToOneField(details, models.DO_NOTHING, db_column='enrollmentno', primary_key=True)

class studentplacedDetails(models.Model):
    enrollmentno = models.CharField(primary_key=True,max_length=11)   
    firstname = models.CharField(blank=True,null=True,max_length=30)
    lastname = models.CharField(blank=True, null=True,max_length=30)
    companyname = models.CharField(blank=True,null=True,max_length=30)
    package = models.FloatField(blank=True, null=True)
    bondterm = models.FloatField(blank=True, null=True)
    typeofjob = models.CharField(blank=True,null=True,max_length=30)
    encode_company = models.CharField(blank=True,null=True,max_length=100)
    
class studentInternshipDetails(models.Model):
    enrollmentno = models.CharField(primary_key=True,max_length=11)   
    firstname = models.CharField(blank=True,null=True,max_length=30)
    lastname = models.CharField(blank=True, null=True,max_length=30)
    companyname = models.CharField(blank=True,null=True,max_length=30)
    stipend = models.PositiveSmallIntegerField(blank=True, null=True)
    typeofjob = models.CharField(blank=True,null=True,max_length=30)
    encode_company = models.CharField(blank=True,null=True,max_length=100)
    
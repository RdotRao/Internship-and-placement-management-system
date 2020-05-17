from django.db import models

# Create your models here.

class internshipplusplacementopportunity(models.Model):
    encode_company = models.CharField(blank=True,null=True,max_length=100)
    companyname = models.CharField(blank=True,null=True,max_length=30)
    typeofjob = models.CharField(blank=True,null=True,max_length=30)
    location= models.CharField(blank=True,null=True,max_length=30)
    preferredlanguages = models.CharField(blank=True,null=True,max_length=30)
    preferredtoolsandtechnologies = models.CharField(blank=True,null=True,max_length=30)
    package = models.FloatField(blank=True, null=True)
    stipend = models.PositiveSmallIntegerField(blank=True, null=True)
    bondterm = models.FloatField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    interviewdate = models.DateField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    last_result = models.CharField(blank=True,null=True,max_length=100)
    def __str__(self):
        return str(self.encode_company)+str(self.companyname)+str(self.typeofjob) + str(self.location) + str(self.package) + str(self.stipend)

class internshipopportunity(models.Model):
    encode_company = models.CharField(blank=True,null=True,max_length=100)
    companyname = models.CharField(blank=True,null=True,max_length=30)
    typeofjob = models.CharField(blank=True,null=True,max_length=30)
    location= models.CharField(blank=True,null=True,max_length=30)
    preferredlanguages = models.CharField(blank=True,null=True,max_length=30)
    preferredtoolsandtechnologies = models.CharField(blank=True,null=True,max_length=30)
    stipend = models.PositiveSmallIntegerField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    interviewdate = models.DateField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    last_result = models.CharField(blank=True,null=True,max_length=100)
    def __str__(self):
        return str(self.encode_company)+str(self.companyname)+str(self.typeofjob) + str(self.location) + str(self.stipend)

class placementopportunity(models.Model):
    encode_company = models.CharField(blank=True,null=True,max_length=100)
    companyname = models.CharField(blank=True,null=True,max_length=30)
    typeofjob = models.CharField(blank=True,null=True,max_length=30)
    location= models.CharField(blank=True,null=True,max_length=30)
    preferredlanguages = models.CharField(blank=True,null=True,max_length=30)
    preferredtoolsandtechnologies = models.CharField(blank=True,null=True,max_length=30)
    package = models.FloatField(blank=True, null=True)
    bondterm = models.FloatField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    interviewdate = models.DateField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    last_result = models.CharField(blank=True,null=True,max_length=100)
    def __str__(self):
        return "Company : "+str(self.companyname) +" |\tType of Job : "+ str(self.typeofjob) +" |\tPackage : "+str(self.package)

class results(models.Model):
    encode_company = models.CharField(blank=True,null=True,max_length=100)
    results_name = models.CharField(blank=True,null=True,max_length=100)
    results_type = models.CharField(blank=True,null=True,max_length=100)
    enrollmentno_name = models.CharField(blank=True,null=True,max_length=200)
    date= models.DateField(blank=True, null=True)

class finalresults(models.Model):
    encode_company = models.CharField(blank=True,null=True,max_length=100)
    opp_type = models.CharField(blank=True,null=True,max_length=100)
    enrollmentno = models.CharField(max_length=11)
    firstname = models.CharField(blank=True,null=True,max_length=30)
    middlename = models.CharField(blank=True, null=True,max_length=30)
    lastname = models.CharField(blank=True, null=True,max_length=30)
    companyname = models.CharField(blank=True,null=True,max_length=30)
    typeofjob = models.CharField(blank=True,null=True,max_length=30)
    location= models.CharField(blank=True,null=True,max_length=30)
    preferredlanguages = models.CharField(blank=True,null=True,max_length=30)
    preferredtoolsandtechnologies = models.CharField(blank=True,null=True,max_length=30)
    package = models.FloatField(blank=True, null=True)
    stipend = models.PositiveSmallIntegerField(blank=True, null=True)
    bondterm = models.FloatField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)


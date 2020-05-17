from django import forms
from .models import details,completeddetails

class DateInput(forms.DateInput):
    input_type = 'date'

class CompletedDetailsForm(forms.Form):
    CHOICES=[('Internship','Intership'),
         ('Both','Both ( Internship + Placement )')]
    internship_or_both = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect,label="Choose One")     

class DetailsForm(forms.Form):
    CHOICES=[('HSC','HSC'),
         ('Diploma','Diploma')]
    GENDER=[('Male','Male'),
            ('Female','Female'),
            ('Others','Others')]
    Specialization=[
        ('BTECH-CSE-BDA','BTECH-CSE-BDA'),
        ('BTECH-CSE-CBA','BTECH-CSE-CBA'),
        ('BTECH-CSE-CS','BTECH-CSE-CS'),
         ]

    enrollmentno = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    firstname = forms.CharField()
    middlename = forms.CharField()
    lastname = forms.CharField()
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect)
    dob = forms.DateField(widget=DateInput)
    phno = forms.IntegerField() 
    parentphno = forms.IntegerField()
    program = forms.CharField(widget=forms.Select(choices=Specialization))
    email = forms.EmailField()
    hsc_or_diploma = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class AcademicDetailsHSCForm(forms.Form):
    ssc_year = forms.IntegerField()
    ssc_percentage = forms.FloatField()
    ssc_board = forms.CharField()
    hsc_year = forms.IntegerField()
    hsc_percentage = forms.FloatField()
    hsc_board = forms.CharField()
    
class AcademicDetailsDiplomaForm(forms.Form):
    ssc_year = forms.IntegerField()
    ssc_percentage = forms.FloatField()
    ssc_board = forms.CharField()
    diploma_year = forms.IntegerField()
    diploma_university = forms.CharField()
    diploma_percentage = forms.FloatField()

class CurrentAcadamicDetailsForm(forms.Form):
    sgpa_sem_1 =  forms.FloatField()
    sgpa_sem_2 =  forms.FloatField()
    sgpa_sem_3 =  forms.FloatField()
    sgpa_sem_4 =  forms.FloatField()
    sgpa_sem_5 =  forms.FloatField()
    sgpa_sem_6 =  forms.FloatField()
    sgpa_sem_7 =  forms.FloatField()
    sgpa_sem_8 =  forms.FloatField()
    cgpa =  forms.FloatField()
    effbacklog = forms.IntegerField()
    

class PlacementDetailsForm(forms.Form):
    skillset = forms.CharField(widget=forms.Textarea)
    cityofinterest =  forms.CharField(widget=forms.Textarea)
    positionofinterest = forms.CharField(widget=forms.Textarea)
    toolsandtechnology = forms.CharField(widget=forms.Textarea)
    photo = forms.FileField()
    resume = forms.FileField()
    sign = forms.FileField()
    linkedinURL = forms.URLField()
    
'''class DetailsForm(forms.ModelForm):
    class Meta:
        model = details
        fields = [
            'enrollmentno',
            'firstname',
    'middlename',
    'lastname',
    'gender',
    'dob',
    'phno',
    'parentphno',
    'program',
    'email']
        
   
class AcademicDetailsForm(forms.ModelForm):
    class Meta:
        model = details
        fields = [
    'ssc_year',
    'ssc_percentage',
    'ssc_board',
    'hsc_year',
    'hsc_percentage',
    'hsc_board',
    'diploma_year',
    'diploma_university',
    'diploma_percentage']

class CurrentAcadamicDetailsForm(forms.ModelForm):
    class Meta:
        model = details
        fields = [
    'sgpa_sem_1',
    'sgpa_sem_2',
    'sgpa_sem_3',
    'sgpa_sem_4',
    'sgpa_sem_5',
    'sgpa_sem_6',
    'sgpa_sem_7',
    'sgpa_sem_8',
    'cgpa']

class PlacementDetailsForm(forms.ModelForm):
    class Meta:
        model = details
        fields = [
    'cityofinterest',
    'skillset',
    'postionofinterest',
    'toolsandtechnology',
    'linkedinURL',
    'effbacklog',
    'resume'
        ]'''

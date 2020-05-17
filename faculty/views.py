from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse 
from django.contrib.auth.models import User,auth
from django.views.decorators.cache import cache_control
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
import pandas as pd
import psycopg2
import os, re, glob
from django.http import HttpResponse
import psycopg2
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from faculty.models import fdetails
from opportunity.models import internshipplusplacementopportunity,internshipopportunity,placementopportunity
from random import seed
from random import randint
from django.shortcuts import render,redirect
from student.models import details,applied,completeddetails,studentInternshipDetails,studentplacedDetails
from opportunity.models import internshipplusplacementopportunity,internshipopportunity,placementopportunity,finalresults
from django.http import HttpResponse
import psycopg2
from django.contrib.auth.models import User,auth
#from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.core.mail import EmailMessage
from random import seed
from random import randint
import base64
from django.db.models import Q
import datetime 
from datetime import date
from opportunity.models import results
from django.http import FileResponse, Http404

@login_required
def uploadothersofferletter(request):
    if request.POST:
        if request.POST.get("Submit") == "first":
            userid = request.POST.get("uid")
            print(userid)
            try:
                userobj = completeddetails.objects.get(enrollmentno=userid)
                if userobj.OfferLetterNotSubmitted:
                    if userobj.placementselected:
                        if userobj.internshipselected:
                            try:
                                studentplacedDetailsobj = studentplacedDetails.objects.get(enrollmentno=userid)
                                studentInternshipDetailsobj = studentInternshipDetails.objects.get(enrollmentno=userid)
                                company_name =  studentplacedDetailsobj.companyname
                                name = studentplacedDetailsobj.firstname
                                job_role = studentplacedDetailsobj.typeofjob
                                package =  studentplacedDetailsobj.package
                                bond = studentplacedDetailsobj.bondterm
                                stipend = studentInternshipDetailsobj.stipend
                                encode_company = studentplacedDetailsobj.encode_company
                                return render(request,'uploadothersofferletterfaculty.html',{"company": company_name,"stipend":stipend,"role":job_role,"package":package,"bond":bond,"opp":encode_company,"name":name,"uid":userid})
                            except Exception as e :
                                error = "Invalid" + str(e)
                                flag  = "True"
                                return render(request,'uploadothersofferletterfaculty.html',{"error":error,"flag":flag})
                        else:        
                                error = "Please Generate NOC First"
                                flag  = "True"
                                return render(request,'uploadothersofferletterfaculty.html',{"error":error,"flag":flag})            
                else:
                    error = "Offer Already Submitted By the Student"
                    flag  = "True"
                    return render(request,'uploadothersofferletterfaculty.html',{"error":error,"flag":flag})            

            except Exception as e :
                error = "Invalid" + str(e)
                flag  = "True"
                return render(request,'uploadothersofferletterfaculty.html',{"error":error,"flag":flag})        
                    
        else:
            userid = request.POST.get("uid")
            try:
                role = request.POST.get('role')
                sal = request.POST.get('sal')
                stipend = request.POST.get('stipend')
                bondterm = request.POST.get('bondterm')
                studentplacedDetailsobj = studentplacedDetails.objects.get(enrollmentno=userid)
                studentInternshipDetailsobj = studentInternshipDetails.objects.get(enrollmentno=userid)
                if role is not None and role != studentplacedDetailsobj.typeofjob:     
                    studentplacedDetailsobj.typeofjob = role
                if sal is not None and sal != studentplacedDetailsobj.package:    
                    studentplacedDetailsobj.package = sal
                if bondterm is not None and studentplacedDetailsobj.bondterm != bondterm:    
                    studentplacedDetailsobj.bondterm = bondterm
                if stipend is not None and stipend != studentInternshipDetailsobj.stipend:    
                    studentInternshipDetailsobj.stipend = stipend
                
                offletter = request.FILES['letter']                
                ext_offerletter = offletter.name.split('.')[-1]
                filename_offerletter = "%s.%s" % (str(userid)+"offerletter", ext_offerletter)
                dir_path = "/Users/rajrao/Desktop/trainingandplacement-master/media/"
                doc_path = "/offerletters"
                with open(dir_path + doc_path + filename_offerletter,'wb') as f:
                    shutil.copyfileobj(offletter,f)
                            
                studentobject = completeddetails.objects.get(enrollmentno=userid)
                studentobject.OfferLetterNotSubmitted = False
                studentobject.reuploadofferletter = False
                studentobject.OfferLetterVerified = False
                studentobject.OfferLetterComment is None
                studentobject.OfferLetter = dir_path + doc_path + filename_offerletter
                studentobject.save()
                studentplacedDetailsobj.save()
                studentInternshipDetailsobj.save()
                msg = "Offer letter Upload Successful"
                flag  = True
                return render(request,'uploadothersofferletterfaculty.html',{"msg":msg,"flag":flag,"not_form":True})
            except Exception as e :
                print(e)
                error = "Invalid" + str(e)
                flag  = "True"
                return render(request,'uploadothersofferletterfaculty.html',{"error":error,"flag":flag,"not_form":True})
    else:    
        flag = True
        if request.session.has_key("uid") and request.session.get("uid")!=None:
            return render(request,'uploadothersofferletterfaculty.html',{"flag":flag})

@login_required
def vol(request):
    if request.method == "POST":
        eno = request.POST.get('eno')
        print(eno)
        completeddetailsobj = completeddetails.objects.get(enrollmentno=eno)
        comment = request.POST.get('comment')
        print(comment)    
        print(request.POST.get(str(eno)+"status"))
        if request.POST.get(str(eno)+"status") is True:
            completeddetailsobj.OfferLetterVerified = True
            completeddetailsobj.reuploadofferletter = False
        else:
            completeddetailsobj.OfferLetterVerified = True
            completeddetailsobj.OfferLetterComment = comment
            completeddetailsobj.reuploadofferletter = True
                      
        completeddetailsobj.save()
        return redirect('/faculty/vol')
    else:    
        completeddetailsobj = completeddetails.objects.exclude(Q(OfferLetterNotSubmitted = "True")|Q(OfferLetterVerified = "True"))
        student_list = []
        flag = False
        for completeddetail in completeddetailsobj:
            student_list.append(completeddetail.enrollmentno)
        print(student_list)
        if len(student_list):
            flag = True
        studentplacedDetailsobj = studentplacedDetails.objects.filter(Q(enrollmentno__in = student_list))
        print(studentplacedDetailsobj)
        return render(request,'verifyofferletterfaculty.html',{"students":studentplacedDetailsobj,"flag":flag})


@login_required
def internshipplusplacement(request):
    username = request.session.get("username")
    if request.method == 'POST':
        companyname = request.POST['companyname']
        typeofjob = request.POST['type']
        encode_company = base64.b64encode(str.encode(companyname+" "+typeofjob+" both"))
        encode_company = encode_company.decode()
        location = request.POST['location']
        preferredlanguages = request.POST['preferredlanguages']
        preferredtoolsandtechnologies = request.POST['preferredtoolsandtechnologies']
        package = request.POST['package']
        stipend = request.POST['stipend']        
        bondterm = request.POST['bondterm']
        deadline = request.POST['deadline']
        #deadline = deadline[8:]+"-"+deadline[5:7] +"-"+deadline[:4]
        interviewdate = request.POST['interviewdate']
        #interviewdate = interviewdate[8:]+"-"+interviewdate[5:7] +"-"+interviewdate[:4]
        details = request.POST.get('details')
        try:
            internshipplusplacementopportunity.objects.get(encode_company=encode_company,companyname=companyname,typeofjob=typeofjob,location=location,preferredlanguages=preferredlanguages,preferredtoolsandtechnologies=preferredtoolsandtechnologies,package=package,stipend=stipend,bondterm=bondterm,deadline=deadline,interviewdate=interviewdate,details=details)
            return render(request,'internshipplusplacement.html',{"username":username,"message":"Opportunity Already Added"}) 
        except internshipplusplacementopportunity.DoesNotExist:
            obj =  internshipplusplacementopportunity(encode_company=encode_company,companyname=companyname,typeofjob=typeofjob,location=location,preferredlanguages=preferredlanguages,preferredtoolsandtechnologies=preferredtoolsandtechnologies,package=package,stipend=stipend,bondterm=bondterm,deadline=deadline,interviewdate=interviewdate,details=details)
            obj.save()
            return render(request,'internshipplusplacementfaculty.html',{"message":"Opportunity Added"}) 

    else:   
        return render(request,'internshipplusplacementfaculty.html')

@login_required
def placement(request):
    username = request.session.get("username")
    if request.method == 'POST':
        companyname = request.POST['companyname']
        typeofjob = request.POST['type']
        encode_company = base64.b64encode(str.encode(companyname+" "+typeofjob+" placement"))
        encode_company = encode_company.decode()
        location = request.POST['location']
        preferredlanguages = request.POST['preferredlanguages']
        preferredtoolsandtechnologies = request.POST['preferredtoolsandtechnologies']
        package = request.POST['package']
        bondterm = request.POST['bondterm']
        deadline = request.POST['deadline']
        #deadline = deadline[8:]+"-"+deadline[5:7] +"-"+deadline[:4]
        interviewdate = request.POST['interviewdate']
        #interviewdate = interviewdate[8:]+"-"+interviewdate[5:7] +"-"+interviewdate[:4]
        details = request.POST.get('details')
        try:
            placementopportunity.objects.get(encode_company=encode_company,companyname=companyname,typeofjob=typeofjob,location=location,preferredlanguages=preferredlanguages,preferredtoolsandtechnologies=preferredtoolsandtechnologies,package=package,bondterm=bondterm,deadline=deadline,interviewdate=interviewdate,details=details)
            return render(request,'placementfaculty.html',{"username":username,"message":"Opportunity Already Added"}) 
        except placementopportunity.DoesNotExist:
            obj =  placementopportunity(encode_company=encode_company,companyname=companyname,typeofjob=typeofjob,location=location,preferredlanguages=preferredlanguages,preferredtoolsandtechnologies=preferredtoolsandtechnologies,package=package,bondterm=bondterm,deadline=deadline,interviewdate=interviewdate,details=details)
            obj.save()
            return render(request,'placementfaculty.html',{"message":"Opportunity Added"}) 
    
    else:    
        return render(request,'placementfaculty.html')

@login_required
def internship(request):
    username = request.session.get("username")
    if request.method == 'POST':
        companyname = request.POST['companyname']
        typeofjob = request.POST['type']
        encode_company = base64.b64encode(str.encode(companyname+" "+typeofjob+" internship"))
        encode_company = encode_company.decode()
        location = request.POST['location']
        preferredlanguages = request.POST['preferredlanguages']
        preferredtoolsandtechnologies = request.POST['preferredtoolsandtechnologies']
        stipend = request.POST['stipend']        
        deadline = request.POST['deadline']
        #deadline = deadline[8:]+"-"+deadline[5:7] +"-"+deadline[:4]
        interviewdate = request.POST['interviewdate']
        #interviewdate = interviewdate[8:]+"-"+interviewdate[5:7] +"-"+interviewdate[:4]
        details = request.POST.get('details')
        try:
            internshipopportunity.objects.get(encode_company=encode_company,companyname=companyname,typeofjob=typeofjob,location=location,preferredlanguages=preferredlanguages,preferredtoolsandtechnologies=preferredtoolsandtechnologies,stipend=stipend,deadline=deadline,interviewdate=interviewdate,details=details)
            return render(request,'internshipfaculty.html',{"message":"Opportunity Already Added"}) 
        except internshipopportunity.DoesNotExist:
            obj =  internshipopportunity(encode_company=encode_company,companyname=companyname,typeofjob=typeofjob,location=location,preferredlanguages=preferredlanguages,preferredtoolsandtechnologies=preferredtoolsandtechnologies,stipend=stipend,deadline=deadline,interviewdate=interviewdate,details=details)
            obj.save()
            return render(request,'internshipfaculty.html',{"message":"Opportunity Added"}) 
    
    else:    
        return render(request,'internshipfaculty.html')

''''
@login_required
def dashboard(request):
    userid = request.session.get("uid")
    detaildata = fdetails.objects.get(empcode=userid)
    bothopportunity = internshipplusplacementopportunity.objects.all()
    internship_opportunity = internshipopportunity.objects.all()
    placement_opportunity = placementopportunity.objects.all()
    return render(request,'facultysuccess.html',{"bothopportunity": bothopportunity,"internship_opportunity":internship_opportunity,"placement_opportunity":placement_opportunity})
'''

@login_required
def dashboard(request):
    completeddetailsobjs = completeddetails.objects.all()
    detailsfilled = 0
    detailsnotfilled = 0 
    placement = 0
    internship = 0
    internshipcompleted = 0
    NOCpending = 0
    OfferLetterPending = 0
    placed = 0
    NotChoosen = 0
    student = 0
    studentc = 0
    for completeddetailsobj in completeddetailsobjs:
        try:
            studentobj = User.objects.get(username=completeddetailsobj.enrollmentno)
            if studentobj.is_staff:
                studentc = studentc + 1
            else:    
                student = student + 1
        except: 
            User.objects.create(username=completeddetailsobj.enrollmentno,password="1234",is_staff=False,is_superuser=False)
        if completeddetailsobj.internshipselected and completeddetailsobj.placementselected:
            if completeddetailsobj.NOCDetails is not None and completeddetailsobj.OfferLetterComment is None and completeddetailsobj.OfferLetterVerified:
                placed = placed + 1                    
                internshipcompleted = internshipcompleted + 1
            else:
                NOCpending = NOCpending + 1
                OfferLetterPending = OfferLetterPending + 1        
        if completeddetailsobj.placement and completeddetailsobj.internship:
            placement = placement + 1
        elif completeddetailsobj.internship:
            internship = internship + 1   
        else:
            NotChoosen = NotChoosen + 1                
        if completeddetailsobj.filleddetails:
            detailsfilled = detailsfilled + 1 
        else:
            detailsnotfilled = detailsnotfilled + 1
    return render(request,'facultysuccess.html',{'detailsfilled':detailsfilled,'detailsnotfilled':detailsnotfilled,'placement':placement,'internship':internship,'internshipcompleted':internshipcompleted,'NOCpending':NOCpending,'OfferLetterPending':OfferLetterPending,'placed':placed,"NotChoosen":NotChoosen,'studentc':studentc,'student':student})
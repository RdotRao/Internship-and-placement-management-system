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
import shutil


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
                                return render(request,'uploadothersofferletter.html',{"company": company_name,"stipend":stipend,"role":job_role,"package":package,"bond":bond,"opp":encode_company,"name":name,"uid":userid})
                            except Exception as e :
                                error = "Invalid" + str(e)
                                flag  = "True"
                                return render(request,'uploadothersofferletter.html',{"error":error,"flag":flag})
                        else:        
                                error = "Please Generate NOC First"
                                flag  = "True"
                                return render(request,'uploadothersofferletter.html',{"error":error,"flag":flag})            
                else:
                    error = "Offer Already Submitted By the Student"
                    flag  = "True"
                    return render(request,'uploadothersofferletter.html',{"error":error,"flag":flag})            

            except Exception as e :
                error = "Invalid" + str(e)
                flag  = "True"
                return render(request,'uploadothersofferletter.html',{"error":error,"flag":flag})        
                    
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
                return render(request,'uploadothersofferletter.html',{"msg":msg,"flag":flag,"not_form":True})
            except Exception as e :
                print(e)
                error = "Invalid" + str(e)
                flag  = "True"
                return render(request,'uploadothersofferletter.html',{"error":error,"flag":flag,"not_form":True})
    else:    
        flag = True
        if request.session.has_key("uid") and request.session.get("uid")!=None:
            return render(request,'uploadothersofferletter.html',{"flag":flag})

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
        return redirect('/studentcoordinator/vol')
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
        return render(request,'verifyofferletter.html',{"students":studentplacedDetailsobj,"flag":flag})

@login_required
def openofferletter(request,student):
    try:
        return FileResponse(open('/Users/rajrao/Desktop/trainingandplacement-master/media/offerletters/'+student+'offerletter.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404() 
    
# Create your views here.
@login_required
def showpassedopportunity(request):
    if request.session.has_key("uid"):
        userid = request.session.get("uid")
        obj = completeddetails.objects.get(enrollmentno = userid)
        today = datetime.datetime.today().date()        
        if obj.internship and obj.placement:
            bothopportunity = internshipplusplacementopportunity.objects.exclude(Q(deadline__gte=today))
            internship_opportunity = internshipopportunity.objects.exclude(Q(deadline__gte=today))
            placement_opportunity = placementopportunity.objects.exclude(Q(deadline__gte=today))
            return render(request,'showpassedopportunity.html',{"bothopportunity": bothopportunity,"internship_opportunity":internship_opportunity,"placement_opportunity":placement_opportunity,"placementflag":"true"})
        else:
            internship_opportunity = internshipopportunity.objects.all()
            return render(request,'showpassedopportunity.html',{"internship_opportunity":internship_opportunity,"internshipflag":"true"})

@login_required
def declareopportunityresult(request,opportunity):
    if request.method=="POST":
        students = str(request.POST.get("students"))
        students = students.split(',')
        print(students)
        encode_company = str(request.POST.get("encode"))
        resulttype = str(request.POST.get("typechoice"))
        resultname =  str(request.POST.get("name"))
        flag=False
        try:
            obj = internshipplusplacementopportunity.objects.get(encode_company=encode_company)
            opp_type = "Internship and Placement"
        except:
            try:
                obj = internshipopportunity.objects.get(encode_company=encode_company)
                opp_type = "Internship"
            except:
                try:
                    obj = placementopportunity.objects.get(encode_company=encode_company)
                    opp_type = "Placement"
                except Exception as e:
                    print(e)
                    return render(request,"error.html")  
        today = date.today()
        week_deadline = today + datetime.timedelta(days=8)
        if resulttype != "Final":
            obj.last_result = resultname + " " + str(today)
        else:
            obj.last_result = resultname    
        obj.save()
        for student in students:
            if resulttype == "Final":
                studenteno = student[0:11]
                print(studenteno)
                studentdetailsobj = details.objects.get(enrollmentno=studenteno)             
                if opp_type == "Internship and Placement":
                    finalresultobj =  finalresults.objects.create(encode_company=encode_company, opp_type= opp_type,enrollmentno=studenteno,firstname=studentdetailsobj.firstname,middlename = studentdetailsobj.middlename,lastname = studentdetailsobj.lastname,companyname=obj.companyname,typeofjob=obj.typeofjob,location=obj.location,preferredlanguages=obj.preferredlanguages,preferredtoolsandtechnologies = obj.preferredtoolsandtechnologies,package = obj.package,stipend = obj.stipend,bondterm=obj.bondterm)                
                elif opp_type == "Internship":
                    finalresultobj =  finalresults.objects.create(encode_company=encode_company, opp_type= opp_type,enrollmentno=studenteno,firstname=studentdetailsobj.firstname,middlename = studentdetailsobj.middlename,lastname = studentdetailsobj.lastname,companyname=obj.companyname,typeofjob=obj.typeofjob,location=obj.location,preferredlanguages=obj.preferredlanguages,preferredtoolsandtechnologies = obj.preferredtoolsandtechnologies,package = None,stipend = obj.stipend,bondterm= None)                                          
                else:    
                    finalresultobj =  finalresults.objects.create(encode_company=encode_company, opp_type= opp_type,enrollmentno=studenteno,firstname=studentdetailsobj.firstname,middlename = studentdetailsobj.middlename,lastname = studentdetailsobj.lastname,companyname=obj.companyname,typeofjob=obj.typeofjob,location=obj.location,preferredlanguages=obj.preferredlanguages,preferredtoolsandtechnologies = obj.preferredtoolsandtechnologies,package = obj.package,stipend = None,bondterm=obj.bondterm)                
            try:
                results_obj = results.objects.get(encode_company=encode_company,results_type=resulttype,results_name=resultname,enrollmentno_name=student,date=today)                    
                flag=True
            except Exception as e:
                print(e)
                flag=False
                results_obj = results.objects.create(encode_company=encode_company,results_type=resulttype,results_name=resultname,enrollmentno_name=student,date=today)    
                continue
        if flag:
            request.session["message"]="Result Already Posted <Possible Duplicate Entry>"        
        else:     
            request.session["message"]="Result Successfully Posted"        
        return redirect('declareresult')
    else:
        try:
            obj = internshipplusplacementopportunity.objects.get(encode_company=opportunity)
            opp_type = "Internship and Placement"
        except:
            try:
                obj = internshipopportunity.objects.get(encode_company=opportunity)
                opp_type = "Internship"
            except:
                try:
                    obj = placementopportunity.objects.get(encode_company=opportunity)
                    opp_type = "Placement"
                except Exception as e:
                    print(e)
                    return render(request,"error.html")  

        if obj.last_result is None:            
            applied_company_obj = applied.objects.filter(encode_company=opportunity)
            opportunity_ = base64.b64decode(opportunity.encode()).decode()
            list_opportunity = opportunity_.split()
            if(list_opportunity[len(list_opportunity)-1]=="both"):
                list_opportunity[len(list_opportunity)-1]="(Placement + Internship)"                            
            opportunity_= " ".join(list_opportunity)
            #opportunity_ = str(list_opportunity)
            if len(applied_company_obj)==0:
                return render(request,'declareopportunityresult.html',{"valid":False,"message": "No Student as Yet Applied"})            
            else:   
                return render(request,'declareopportunityresult.html',{"valid":True,"opportunity": applied_company_obj,"opportunity_details":opportunity_,"encode":opportunity})        
        else:
            temp = obj.last_result.split()
            tmp = []
            for i in temp:
	            for j in i:
		            if (ord(j)>64 and ord(j)<91)or (ord(j)>96 and ord(j)<123):
			            if i not in tmp:
				            tmp.append(i)
            results_name = " ".join(tmp)
            print(results_name)
            applied_company_obj = results.objects.filter(Q(results_name=results_name)&Q(encode_company=opportunity))
            opportunity_ = base64.b64decode(opportunity.encode()).decode()
            list_opportunity = opportunity_.split()
            if(list_opportunity[len(list_opportunity)-1]=="both"):
                list_opportunity[len(list_opportunity)-1]="(Placement + Internship)"                            
            opportunity_= " ".join(list_opportunity)
            #opportunity_ = str(list_opportunity)
            if len(applied_company_obj)==0:
                return render(request,'declareopportunityresult.html',{"valid":False,"message": "Invalid Opportunity"})            
            else:   
                return render(request,'declareopportunityresult.html',{"valid":True,"opportunity": applied_company_obj,"opportunity_details":opportunity_,"encode":opportunity,"flag":True})
def declareresult(request):
        today = datetime.datetime.today().date()  
        message = ""
        if request.session.has_key("message"):
            message = request.session.get("message")
            del request.session['message']                              

        bothopportunity = internshipplusplacementopportunity.objects.exclude(Q(interviewdate__gt=today)|Q(last_result="FINAL"))
        internship_opportunity = internshipopportunity.objects.exclude(Q(interviewdate__gt=today)|Q(last_result="FINAL"))
        placement_opportunity = placementopportunity.objects.exclude(Q(interviewdate__gt=today)|Q(last_result="FINAL"))
        return render(request,'declareresults.html',{"bothopportunity": bothopportunity,"internship_opportunity":internship_opportunity,"placement_opportunity":placement_opportunity,"message":message,"flag":"Not Declared"})



def getDetail(uid,request):
    userid = request.session.get("uid")
    detaildata = details.objects.get(enrollmentno=userid)
    userData = {"detaildata":detaildata}
    return userData

@login_required
def dashboard(request):
    if request.method == 'POST':
        userid = request.session.get("uid")
        detaildata = details.objects.get(enrollmentno=userid)
        print(request.POST['otp'] == request.session.get('otp'))
        print(request.POST['dob']==str(detaildata.dob))
        print(request.POST['dob'])
        print(detaildata.dob)
        print(request.POST['otp'])
        print(request.session.get('OTP'))
        if (str(request.POST['otp']) == str(request.session.get('OTP')) and request.POST['dob']==str(detaildata.dob)):
            obj = User.objects.get(username=userid)
            obj.set_password(request.POST['pass'])
            obj.save()
            del request.session['firstlogin']
            del request.session['email']
            return redirect('/passwordchangesuccessfull')              
        else:
            return render(request,'changepassword.html',{"message":"OTP or DOB Mismatch"})    
    else:    
        if(request.session.has_key("firstlogin") and request.session.has_key("email")):
            if(request.session.get("firstlogin")== "True"):
                try:    
                    #seed(100)
                    otp = randint(10000, 99999)
                    print(otp)
                    userid = request.session.get("uid")
                    detaildata = details.objects.get(enrollmentno=userid)
                    print(detaildata.dob)
                    request.session["OTP"] = otp
                    print(request.session.get("email"))
                    email = EmailMessage('OTP', 'Your OTP for password change is :- '+str(otp), to=[request.session.get("email")])
                    email.send()
                except Exception as e: print(e)
                return render(request,'changepassword.html')    
        else:
            username = request.session.get("username")
            userid = request.session.get("uid")
            try:
                obj = completeddetails.objects.get(enrollmentno = userid)
            except completeddetails.DoesNotExist:
                obj = completeddetails.objects.create(enrollmentno = userid)
            obj = completeddetails.objects.get(enrollmentno = userid)
            print(obj.filleddetails)
            if obj.filleddetails:
                if obj.internshipselected and obj.placementselected:
                    OfferLetterNotSubmitted = False
                    if obj.OfferLetterNotSubmitted:
                        OfferLetterNotSubmitted = True
                    studentInternshipDetailsObj = studentInternshipDetails.objects.get(enrollmentno=userid)
                    studentplacedDetailsObj = studentplacedDetails.objects.get(enrollmentno=userid)
                    message1 = "You have already selected "+ studentplacedDetailsObj.companyname + " for Placement"
                    message2 = "You have already selected "+ studentInternshipDetailsObj.companyname + " for Intership"
                    message3 = "Sorry, Now you can't apply or see other opportunities, Thank You" 
                    return render(request,'studsuccess.html',{"message1":message1,"message2":message2,"message3":message3,"placedflag":"true","OfferLetterNotSubmitted":OfferLetterNotSubmitted})
                elif obj.internshipselected:
                    if obj.placement:
                        studentInternshipDetailsObj = studentInternshipDetails.objects.get(enrollmentno=userid)
                        message2 = "You have already selected "+ studentInternshipDetailsObj.companyname + " for Internship"
                        message3 = "Sorry, Now you can't apply or see other opportunities, Thank You" 
                        message = ""
                        if request.session.has_key("message"):
                            message = request.session.get("message")
                            del request.session['message']
                        obj = applied.objects.filter(Q(enrollmentno=userid))
                        loops = len(obj)
                        applied_company_encode = []
                        for i in range(0,loops):
                            applied_company_encode.append(obj[i].encode_company)
                        applied_company_encode = list(set(applied_company_encode))
                        today = datetime.datetime.today().date()        
                        placement_opportunity = placementopportunity.objects.exclude(Q(encode_company__in=applied_company_encode)|Q(deadline__lt=today)|(~Q(last_result=None)))
                        return render(request,'studsuccess.html',{"message2":message2,"message3":message3,"placement_opportunity":placement_opportunity,"message":message,"date":today,"placementflag":"true","intflag":"true"})
                    else:
                        studentInternshipDetailsObj = studentInternshipDetails.objects.get(enrollmentno=userid)
                        message2 = "You have already selected "+ studentInternshipDetailsObj.companyname + " for Internship"
                        message3 = "Sorry, Now you can't apply or see other opportunities" 
                        return render(request,'studsuccess.html',{"message2":message2,"message3":message3,"placedflag":"true"})
                elif obj.placementselected:
                    if obj.internship:
                        redmessage=""
                        message = ""
                        if request.session.has_key("message"):
                            message = request.session.get("message")
                            del request.session['message']
                        obj = applied.objects.filter(Q(enrollmentno=userid))
                        loops = len(obj)
                        applied_company_encode = []
                        for i in range(0,loops):
                            applied_company_encode.append(obj[i].encode_company)
                        applied_company_encode = list(set(applied_company_encode))
                        today = datetime.datetime.today().date()        
                        studentplacedDetailsObj = studentplacedDetails.objects.get(enrollmentno=userid)
                        message1 = "You have already selected "+ studentplacedDetailsObj.companyname + " for Placement"
                        message3 = "Sorry, Now you can't apply or see other opportunities, Thank You" 
                        internship_opportunity = internshipopportunity.objects.exclude(Q(encode_company__in=applied_company_encode)|Q(deadline__lt=today)|(~Q(last_result=None)))
                        return render(request,'studsuccess.html',{"message1":message1,"message3":message3,"internship_opportunity":internship_opportunity,"message":message,"date":today,"placementflag":"true","placflag":"true"})
    
                else:
                    if obj.internship and obj.placement:
                        message = ""
                        if request.session.has_key("message"):
                            message = request.session.get("message")
                            del request.session['message']
                        obj = applied.objects.filter(Q(enrollmentno=userid))
                        loops = len(obj)
                        applied_company_encode = []
                        for i in range(0,loops):
                            applied_company_encode.append(obj[i].encode_company)
                        applied_company_encode = list(set(applied_company_encode))
                        today = datetime.datetime.today().date()        
                        bothopportunity = internshipplusplacementopportunity.objects.exclude(Q(encode_company__in=applied_company_encode)|Q(deadline__lt=today)|(~Q(last_result=None)))
                        internship_opportunity = internshipopportunity.objects.exclude(Q(encode_company__in=applied_company_encode)|Q(deadline__lt=today)|(~Q(last_result=None)))
                        placement_opportunity = placementopportunity.objects.exclude(Q(encode_company__in=applied_company_encode)|Q(deadline__lt=today)|(~Q(last_result=None)))
                        return render(request,'studsuccess.html',{"bothopportunity": bothopportunity,"internship_opportunity":internship_opportunity,"placement_opportunity":placement_opportunity,"message":message,"date":today,"placementflag":"true"})
                    else:
                        #obj = applied.objects.get(enrollmentno=userid)
                        message = ""
                        if request.session.has_key("message"):
                            message = request.session.get("message")
                            del request.session['message']
                        obj = applied.objects.filter(Q(enrollmentno=userid))
                        loops = len(obj)
                        applied_company_encode = []
                        for i in range(0,loops):
                            applied_company_encode.append(obj[i].encode_company)
                        applied_company_encode = list(set(applied_company_encode))
                        today = datetime.datetime.today().date()        
                        internship_opportunity = internshipopportunity.objects.exclude(Q(encode_company__in=applied_company_encode)|Q(deadline__lt=today)|(~Q(last_result=None)))
                        return render(request,'studsuccess.html',{"internship_opportunity":internship_opportunity,"message":message,"date":today,"internshipflag":"true"})
            else:
                return redirect('choose')              


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
            return render(request,'internshipplusplacement.html',{"message":"Opportunity Added"}) 

    else:   
        return render(request,'internshipplusplacement.html')

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
            return render(request,'placement.html',{"username":username,"message":"Opportunity Already Added"}) 
        except placementopportunity.DoesNotExist:
            obj =  placementopportunity(encode_company=encode_company,companyname=companyname,typeofjob=typeofjob,location=location,preferredlanguages=preferredlanguages,preferredtoolsandtechnologies=preferredtoolsandtechnologies,package=package,bondterm=bondterm,deadline=deadline,interviewdate=interviewdate,details=details)
            obj.save()
            return render(request,'placement.html',{"message":"Opportunity Added"}) 
    
    else:    
        return render(request,'placement.html')

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
            return render(request,'internship.html',{"message":"Opportunity Already Added"}) 
        except internshipopportunity.DoesNotExist:
            obj =  internshipopportunity(encode_company=encode_company,companyname=companyname,typeofjob=typeofjob,location=location,preferredlanguages=preferredlanguages,preferredtoolsandtechnologies=preferredtoolsandtechnologies,stipend=stipend,deadline=deadline,interviewdate=interviewdate,details=details)
            obj.save()
            return render(request,'internship.html',{"message":"Opportunity Added"}) 
    
    else:    
        return render(request,'internship.html')

@login_required
def showinternship(request):
    internship_opportunity = internshipopportunity.objects.all()
    return render(request,'showinternship.html',{"internship_opportunity":internship_opportunity})

@login_required
def showplacement(request):
    placement_opportunity = placementopportunity.objects.all()
    return render(request,'showplacement.html',{"placement_opportunity":placement_opportunity})

@login_required
def viewprofile(request):
    userid = request.session.get("uid")
    obj = model_to_dict(details.objects.get(enrollmentno=userid))
    print(obj)
    return render(request,'viewprofile.html',{"details":obj}) 


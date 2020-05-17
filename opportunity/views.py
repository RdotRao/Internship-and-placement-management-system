from django.shortcuts import render,redirect
from django.http import HttpResponse
from fpdf import FPDF
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
import base64
from django.db.models import Q
from .models import internshipplusplacementopportunity,internshipopportunity,placementopportunity,results,finalresults
from student.models import details,applied,completeddetails,studentplacedDetails, studentInternshipDetails
# Create your views here.
import xlwt 
from xlwt import Workbook 
import datetime
import io
from django.http import FileResponse
from django.shortcuts import render,redirect
from student.models import details,completeddetails,position,applied
from opportunity.models import internshipplusplacementopportunity,internshipopportunity,placementopportunity
from django.http import HttpResponse
import psycopg2
from django.contrib.auth.models import User,auth
#from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
import hashlib
from django.conf import settings
import base64
from django.db.models import Q
import shutil
import datetime
from django.http import HttpResponse,Http404
from django.views.generic import View


@login_required
def viewprofile(request):
    userid = request.session.get("uid")
    obj = model_to_dict(details.objects.get(enrollmentno=userid))
    print(obj)
    return render(request,'viewprofile.html',{"details":obj}) 

@login_required
def showpassedopportunity(request):
    if request.session.has_key("uid"):
        userid = request.session.get("uid")
        today = datetime.datetime.today().date()        
        bothopportunity = internshipplusplacementopportunity.objects.exclude(Q(deadline__gte=today))
        internship_opportunity = internshipopportunity.objects.exclude(Q(deadline__gte=today))
        placement_opportunity = placementopportunity.objects.exclude(Q(deadline__gte=today))        
        try:
            obj = completeddetails.objects.get(enrollmentno = userid)
            if obj.internship and obj.placement:
                return render(request,'showpassedopportunity.html',{"bothopportunity": bothopportunity,"internship_opportunity":internship_opportunity,"placement_opportunity":placement_opportunity,"placementflag":"true"})
            else:
                return render(request,'showpassedopportunity.html',{"internship_opportunity":internship_opportunity,"internshipflag":"true"})
        except:
            if len(userid)==6:
                return render(request,'showpassedopportunityfaculty.html',{"bothopportunity": bothopportunity,"internship_opportunity":internship_opportunity,"placement_opportunity":placement_opportunity,"placementflag":"true"})
            else:
                return redirect('/login')    

class PDF(FPDF):
    def header(self):
        # Logo
        logo = "/Users/rajrao/Desktop/trainingandplacement-master/logo.jpg"
        self.image(logo, x=122, y=9, w=70, h=30)
        
    # Page footer
    def footer(self):
        text1 = '(This is an electronically generated NOC, hence does not require signature)'
        text2 = 'Ganpat University,  Ganpat Vidyanagar, Mehsana-Gozaria Highway, PO - 384012, Gujarat, India'
        text3 = 'Phone Number : +91-2762-226000/+91-2762-286080,286924 Toll Free No :1800 233 12345'
        # Position at 1.5 cm from bottom
        self.set_font('Arial', 'BUI', 9)
        self.set_y(-23)
        self.cell(0, 13, text1, 0, 0, 'C')
        self.set_font('Arial', 'BI', 9)
        self.set_y(-19)
        self.cell(0, 13, text2, 0, 0, 'C')    
        self.set_y(-15)
        self.cell(0, 13, text3, 0, 0, 'C')
        
        



def downloadapplied(request,opportunity):
    xlsHeaders=[ "Enrollment No.","First Name","Middle Name","Last Name"
            ,"Gender","Date of Birth","Contact No.","Parent Contact no."
            ,"Program","Email","SSC Year","SSC Percentage","SSC Board"
            ,"HSC Year","HSC Percentage","HSC Board","Diploma Year"
            ,"Diploma University","Diploma Percentage","SGPA Semester 1"
            ,"SGPA Semester 2","SGPA Semester 3","SGPA Semester 4"
            ,"SGPA Semester 5","SGPA Semester 6","SGPA Semester 7","SGPA Semester 8","CGPA" 
            ,"City of Interest","Skillset","Position of Interest","Tools and Technology" 
            ,"Linkedin URL","Effective Backlog"] 
    encode_company = opportunity
    students = applied.objects.filter(Q(encode_company=encode_company))    
    wb = Workbook() 
    countCols = 0
    sheet1 = wb.add_sheet("Sheet 1",cell_overwrite_ok=True) 
    style = xlwt.easyxf('font: bold 1;') 
    for header in xlsHeaders:
        sheet1.write(0,countCols,str(header),style)
        countCols = countCols + 1
    
    countCols = 0
    countRows = 1
    
    for student in students: 
        obj = model_to_dict(details.objects.get(enrollmentno=student.enrollmentno))
        del obj["resume"]
        del obj["photo"]
        del obj["sign"]
        countCols=0 
        for key in obj:
            if obj[key] is None:
                sheet1.write(countRows,countCols,"Not Applicable")
            else:                
                sheet1.write(countRows,countCols,str(obj[key]))
                countCols=countCols+1
        countRows = countRows + 1
        countCols = 0
    opportunity_name = base64.b64decode(opportunity.encode()).decode()    
    wb.save('/Users/rajrao/Desktop/trainingandplacement-master/media/opportunity/'+str(opportunity_name)+'.xls')
   # return render(request,"downloadallapplied.html",{"filename":'/Users/rajrao/Desktop/trainingandplacement-master/media/opportunity/'+str(opportunity_name)+'.xls'})
    return FileResponse(open('/Users/rajrao/Desktop/trainingandplacement-master/media/opportunity/'+str(opportunity_name)+'.xls', 'rb'), content_type='application/excel')
    #return HttpResponse(request,"<a href="{{filename}}" download>Click</a>",{"filename":'/Users/rajrao/Desktop/trainingandplacement-master/media/opportunity/'+str(opportunity_name)+'.xls'})
    #<a href="{{filename}}" download>Click</a>
    #return FileResponse(as_attachment=True, filename='C:/Users/admin/Desktop/'+str(opportunity_name)+'.xls')

#def downloadappliedopp(request,opportunity):


def Applied(request):
    bothopportunity = internshipplusplacementopportunity.objects.all()
    internship_opportunity = internshipopportunity.objects.all()
    placement_opportunity = placementopportunity.objects.all()
    return render(request,'downloadApplied.html',{"bothopportunity": bothopportunity,"internship_opportunity":internship_opportunity,"placement_opportunity":placement_opportunity})

@login_required
def showresult(request):
    if request.session.has_key("uid") and request.session.get("uid")!=None:
        completeddetailsobj = completeddetails.objects.get(enrollmentno=request.session.get("uid"))
        bothopportunity = internship_opportunity = placement_opportunity = None
        if completeddetailsobj.placement:
            bothopportunity = internshipplusplacementopportunity.objects.exclude(Q(last_result=None))
            internship_opportunity = internshipopportunity.objects.exclude(Q(last_result=None))
            placement_opportunity = placementopportunity.objects.exclude(Q(last_result=None))
            return render(request,'showresults.html',{"bothopportunity": bothopportunity,"internship_opportunity":internship_opportunity,"placement_opportunity":placement_opportunity})
        else:
            internship_opportunity = internshipopportunity.objects.exclude(Q(last_result=None))    
            return render(request,'showresults.html',{"internship_opportunity":internship_opportunity,"int_flag":True})
    else:
        return redirect('/login')    

def seedetailopportunityresult(request,resulttype):
    if request.session.has_key("uid") and request.session.get("uid")!=None:
        enrollmentno_name = str(request.session.get("uid"))+" "+name
        details_obj = details.objects.get(enrollmentno=request.session.get("uid"))
        name = str(details_obj.firstname)+" "+str(details_obj.lastname)
        print(enrollmentno_name)
        
    return render(request,'showresults.html')


@login_required
def seeopportunityresult(request,opportunity):
    if request.session.has_key("uid") and request.session.get("uid")!=None:
        encode_company = opportunity
        message=""
        details_obj = details.objects.get(enrollmentno=request.session.get("uid"))
        name = str(details_obj.firstname)+" "+str(details_obj.lastname)
        enrollmentno_name = str(request.session.get("uid"))+" "+name
        results_obj = results.objects.filter(Q(encode_company=encode_company)&Q(enrollmentno_name=enrollmentno_name))        
        last_result_student_obj = results.objects.filter(enrollmentno_name=enrollmentno_name).last()
        last_result_obj = results.objects.filter(encode_company=encode_company).last()
        if len(results_obj) == 0 :
            message = "Sorry, You were not selected in "+ str(last_result_obj.results_name) +" round"
            return render(request,'seeopportunityresult.html',{"results":results_obj,"message":message})
        else:
            if(last_result_student_obj.results_name!=last_result_obj.results_name):
                message = "Sorry, You were not selected in "+ str(last_result_obj.results_name) +" round"
            elif(last_result_student_obj.results_name==last_result_obj.results_name)and last_result_obj.results_name=="FINAL":
                message = "Congrats, You were selected in "+ str(last_result_obj.results_name) +" round."
                message2 = "Generate NOC and Upload offer ASAP."
                return render(request,'seeopportunityresult.html',{"results":results_obj,"message":message,"msg":message2,"flag":True})
            else:
                message = "Other Rounds Pending"                    
            return render(request,'seeopportunityresult.html',{"results":results_obj,"message":message})
        
@login_required
def takeopportunity(request,opportunity):
    if request.session.has_key("uid") and request.session.get("uid")!=None:
        if request.POST:
            encode_company = request.POST.get('encode_company')
            details_obj = details.objects.get(enrollmentno = request.session.get("uid"))
            applied.objects.create(encode_company=encode_company,enrollmentno = request.session.get("uid"),name=str(details_obj.firstname)+" "+str(details_obj.lastname))
            request.session["message"]="Successfully Applied"
            return redirect('/login')
        else:   
            try:
                user_valid = completeddetails.objects.get(enrollmentno=request.session.get("uid"))
                temp_opportunity = opportunity
                opportunity = base64.b64decode(opportunity.encode()).decode()
                list_opportunity = opportunity.split()
                print(list_opportunity)
                opportunity_type = list_opportunity[len(list_opportunity)-1]
                try:
                    obj = model_to_dict(internshipplusplacementopportunity.objects.get(encode_company=temp_opportunity))        
                except Exception as e:
                    try:
                        obj = model_to_dict(internshipopportunity.objects.get(encode_company=temp_opportunity))
                    except Exception as e:        
                        try:
                            obj = model_to_dict(placementopportunity.objects.get(encode_company=temp_opportunity))
                        except Exception as e:        
                            print(e)
                            return render(request,"error.html",e)        
            except Exception as e:
                print(e)
                return render(request,"error.html",e)        
            try:
                encode_company = obj.get("encode_company")
                obj.pop("id")    
                obj.pop("encode_company")    
            except KeyError:
                print("Key not found")    
            context = { "opportunity" :obj ,
                        "encode_company" : encode_company,
                        "applied": False,
                        }
            return render(request,"takeopportunity.html",context)

@login_required
def generateNOC(request):
    if request.session.has_key("uid") and request.session.get("uid")!=None:
        userid = request.session.get("uid")
        userobj = completeddetails.objects.get(enrollmentno=userid)
        if userobj.internshipselected:
            studentInternshipDetailsObj = studentInternshipDetails.objects.get(enrollmentno=userid)
            message2 = "You have already selected "+ studentInternshipDetailsObj.companyname + " for Internship"
            message3 = "Sorry, Now you can't generated new NOC"
            return render(request,'generateNOCform1.html',{"message2":message2,"message3":message3,"placedflag":"true","encode_company":studentInternshipDetailsObj.encode_company})
        else:    
            today = datetime.datetime.today().date()                       
            opp_type = ["Internship and Placement", "Internship"]
            finalresultsobj = finalresults.objects.filter(Q(enrollmentno=userid)&Q(opp_type__in=opp_type))
            return render(request,'generateNOCform1.html',{"opportunities": finalresultsobj,"date":today})
    else:    
        return redirect('/login')

@login_required
def generateNOC_Next(request,opportunity):
    if request.session.has_key("uid") and request.session.get("uid")!=None:
        userid = request.session.get("uid")
        job_role = opp_type = company_name = error = None
        flag  = False
        
        if opportunity == "self_applied_company":
            print("e")
        else:
            companyobj = finalresults.objects.filter(Q(enrollmentno=userid)&Q(encode_company=opportunity))
            if len(companyobj)==0:
                error = "Invalid Opportunity or Broken URL "+str(opportunity)
                flag  = "True"
            else:    
                for company in companyobj:
                    opp_type = company.opp_type
                    company_name =  company.companyname
                    job_role = company.typeofjob
                    package = company.package
                    bond = company.bondterm
                    stipend = company.stipend
                    encode_company = company.encode_company
            return render(request,'generateNOCChoice.html',{"company": company_name,"type":opp_type,"error":error,"flag":flag,"role":job_role,"package":package,"bond":bond,"stipend":stipend,"opp":encode_company})
    else:    
        return redirect('/login')

@login_required
def openOL(request):
    if request.session.has_key("uid") and request.session.get("uid")!=None:
        userid = request.session.get("uid")        
        try:
            return FileResponse(open('/Users/rajrao/Desktop/trainingandplacement-master/media/offerletters/'+str(userid)+'offerletter.pdf', 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            return render(request,"notapplicable.html")
    else:    
        return redirect('/login')


@login_required
def openNOC(request):
    if request.session.has_key("uid") and request.session.get("uid")!=None:
        userid = request.session.get("uid")        
        try:
            return FileResponse(open('/Users/rajrao/Desktop/trainingandplacement-master/media/NOC'+str(userid)+'.pdf', 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404() 
    else:    
        return redirect('/login')
@login_required
def generateNOC_final(request,opportunity):
    if 1==0:
        if 1==0:
            return redirect('/login')
        elif 1==0:
           return None             
    else:  
        if request.session.has_key("uid") and request.session.get("uid")!=None:
            userid = request.session.get("uid")
            companyobj = finalresults.objects.filter(Q(enrollmentno=userid)&Q(encode_company=opportunity))
            company_name = error = None
            flag  = False
            if len(companyobj)==0:
                error = "Invalid Opportunity or Broken URL "+str(opportunity)
                flag  = "True"
            else:    
                for company in companyobj:
                    company_name =  company.companyname
                    name = str(company.firstname) + " " + str(company.lastname )       
                    stipend = company.stipend
                    package = company.package
                    bondterm = company.bondterm
                    opp_type = company.opp_type
                    job_role = company.typeofjob
                    encode_company = company.encode_company
            pdf = PDF()
            pdf.add_page()
            pdf.set_font('Times', '', 12)
            pdf.ln(50)
            pdf.cell(12, 12, txt="Date: 13-11-2020", align="L")
            pdf.ln(6)
            pdf.set_font("times",'BU',size=14)
            pdf.cell(190, 12, txt="No Objection Certificate", align="C")
            pdf.ln(10)
            pdf.set_font("times", size=14)
            pdf.cell(450, 12, txt="This is to certify that the following final year undergraduate student U.V. PATEL COLLEGE", align="L")
            pdf.ln(9)
            pdf.cell(450, 12, txt="OF ENGINEERING, GANPAT UNIVERSITY wishes to apply for an internship at ", align="L")
            pdf.ln(9)
            pdf.cell(450, 12, txt=str(company_name), align="L")
            pdf.ln(9)
            pdf.cell(450, 12, txt="The Institute has no objection in him undergoing a internship program at your prominent", align="L")
            pdf.ln(9)
            pdf.cell(67, 12, txt="organization during the period of", align="L")
            pdf.set_font("times",'BU',size=14)
            pdf.cell(70, 12, txt="09 DECEMBER 2019 TO 10TH APRIL 2020.", align="L")
            pdf.ln(11)
            data_header = ['Sr. No.', 'Name of Students', 'Branch', 'Specialization']
            data1 = ['1.', str(name), 'B Tech - Computer','Cloud Based']
            data2 = [' ', ' ','Science & Engineering', ' Application']
            data3 = [' ', ' ',' ', ' ']
            pdf.set_font("times",'B',size=14)
            for dataitem in range(0,len(data_header)):    
                if dataitem == 2:
                    pdf.cell(55, 12 ,txt=data_header[dataitem], border=1, align="C")
                else:
                    pdf.cell(45, 12 ,txt=data_header[dataitem], border=1, align="C")    
            pdf.set_font("times",size=14)
            pdf.ln(12)
            for dataitem in range(0,len(data_header)):    
                if dataitem == 2:
                    pdf.cell(55, 26 ,txt=data1[dataitem], border=1, align="C")
                else:
                    pdf.cell(45, 26 ,txt=data1[dataitem], border=1, align="C")    
            pdf.ln(12)         
            for dataitem in range(0,len(data_header)):    
                if dataitem == 2:
                    pdf.cell(55, 12 ,txt=data2[dataitem], border=0, align="C")
                else:
                    pdf.cell(45, 12 ,txt=data2[dataitem], border=0, align="C")    
            pdf.ln(12)         
            for dataitem in range(0,len(data_header)):    
                if dataitem == 2:
                    pdf.cell(55, 12 ,txt=data3[dataitem], border=0, align="C")
                else:
                    pdf.cell(45, 12 ,txt=data3[dataitem], border=0, align="C")    
            pdf.ln(52)         
            pdf.cell(450, 12 ,txt="With best regards,",align="L")
            pdf.ln(9)         
            pdf.cell(450, 12 ,txt="Prof. Rahul B Shrimali",align="L")
            pdf.ln(9)         
            pdf.cell(450, 12 ,txt="Training & Placement Officer",align="L")
            pdf.ln(9)         
            pdf.cell(450, 12 ,txt="Department of Computer Science & Engineering, UVPCE, Ganpat University",align="L")
            pdf.output("a.pdf")
            studentobject = completeddetails.objects.get(enrollmentno=userid)
            pdf.output("/Users/rajrao/Desktop/trainingandplacement-master/media/NOC"+str(userid)+".pdf")
            studentobject.NOCgenerated = True
            studentobject.NOCDetails = "/Users/rajrao/Desktop/trainingandplacement-master/media/NOC"+str(userid)+".pdf"
            #filename_ = "NOC"+str(userid)+".pdf"
            buffer = io.BytesIO()
            buffer.seek(0)
            name = name.split(" ")
            if opp_type == "Internship and Placement":
                studentobject.placementselected = studentobject.internshipselected = True
                studentplacedDetails.objects.create(enrollmentno=userid,firstname=str(name[0]),lastname=str(name[1]),companyname=company_name,package=package,bondterm = bondterm,encode_company=encode_company,typeofjob=job_role)
                studentInternshipDetails.objects.create(enrollmentno=userid,firstname=str(name[0]),lastname=str(name[1]),companyname=company_name,stipend=stipend,encode_company=encode_company,typeofjob=job_role)
            elif opp_type == "Internship":
                studentobject.internshipselected = True
                studentInternshipDetails.objects.create(enrollmentno=userid,firstname=str(name[0]),lastname=str(name[1]),companyname=company_name,stipend=stipend,encode_company=encode_company,typeofjob=job_role)
            else:
                studentobject.placementselected = True
                studentplacedDetails.objects.create(enrollmentno=userid,firstname=str(name[0]),lastname=str(name[1]),companyname=company_name,package=package,bondterm = bondterm,encode_company=encode_company,typeofjob=job_role)
                
            studentobject.save()
            
            userid = request.session.get("uid")
            userobj = completeddetails.objects.get(enrollmentno=userid)
            if userobj.internshipselected:
                studentInternshipDetailsObj = studentInternshipDetails.objects.filter(Q(enrollmentno=userid)&Q(encode_company=opportunity))
                company_name = error = None
                flag  = False
                if len(studentInternshipDetailsObj)==0:
                    error = "Invalid Opportunity or Broken URL /opportunity/generateNOC_final/"+str(opportunity)+" Try Again From Home Page"
                    flag  = "True"
                    return render(request,'generateNOC_final.html',{"error":error,"flag":flag})            
                else:    
                    companyobj = finalresults.objects.filter(Q(enrollmentno=userid)&Q(encode_company=opportunity))
                    company_name = error = None
                    if len(companyobj)==0:
                        error = "Invalid Opportunity or Broken URL /opportunity/generateNOC_final/"+str(opportunity)+" Try Again From Home Page"
                        flag  = "True"
                        return render(request,'generateNOC_final.html',{"error":error,"flag":flag})            
                    else:    
                        for company in companyobj:
                            company_name =  company.companyname
                            name = company.firstname + " " +company.lastname        
                            fname = company.firstname
                            lname = company.lastname        
                            encode_company = company.encode_company
                        return render(request,'generateNOC_final.html',{"company":company_name,"student_name":name,"error":error,"flag":flag,"encode_company":encode_company})
                    
            else:
                companyobj = finalresults.objects.filter(Q(enrollmentno=userid)&Q(encode_company=opportunity))
                company_name = error = None
                flag  = False
                if len(companyobj)==0:
                    error = "Invalid Opportunity or Broken URL /opportunity/generateNOC_final/"+str(opportunity)+"                  Try Again From Home Page"
                    flag  = "True"
                    return render(request,'generateNOC_final.html',{"error":error,"flag":flag})
            
                else:    
                    for company in companyobj:
                        company_name =  company.companyname
                        name = str(company.firstname) + " " + str(company.lastname)
                        fname = company.firstname
                        lname = company.lastname        
                        encode_company = company.encode_company
                    return render(request,'generateNOC_final.html',{"company":company_name,"student_name":name,"error":error,"flag":flag,"encode_company":encode_company})

@login_required
def openofferletter(request,student):
    try:
        return FileResponse(open('/Users/rajrao/Desktop/trainingandplacement-master/media/offerletters/'+student+'offerletter.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404() 


@login_required
def uploadofferletter(request):
    if request.POST:
        userid = request.session.get("uid")
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
            dir_path = "/Users/rajrao/Desktop/trainingandplacement-master/media"
            doc_path = "/offerletters/"
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
            error = "Offer letter Upload Successful"
            flag  = "True"
            return render(request,'offeruploadform.html',{"error":error,"flag":flag,"Not_Show":True})
        except Exception as e :
            print(e)
            error = "Invalid" + str(e)
            flag  = "True"
            return render(request,'offeruploadform.html',{"error":error,"flag":flag})
    else:    
        if request.session.has_key("uid") and request.session.get("uid")!=None:
            userid = request.session.get("uid")
            userobj = completeddetails.objects.get(enrollmentno=userid)
            if userobj.OfferLetterNotSubmitted:
                if userobj.placementselected:
                    if userobj.internshipselected:
                        try:
                            studentplacedDetailsobj = studentplacedDetails.objects.get(enrollmentno=userid)
                            studentInternshipDetailsobj = studentInternshipDetails.objects.get(enrollmentno=userid)
                            company_name =  studentplacedDetailsobj.companyname
                            job_role = studentplacedDetailsobj.typeofjob
                            package =  studentplacedDetailsobj.package
                            bond = studentplacedDetailsobj.bondterm
                            stipend = studentInternshipDetailsobj.stipend
                            encode_company = studentplacedDetailsobj.encode_company
                            flag  = "True"
                            return render(request,'offeruploadform.html',{"company": company_name,"stipend":stipend,"role":job_role,"package":package,"bond":bond,"opp":encode_company,"flag":flag})
                        except Exception as e :
                            error = "Invalid" + str(e)
                            flag  = "True"
                            return render(request,'offeruploadform.html',{"error":error,"flag":flag})
                    else:        
                            error = "Please Generate NOC First"
                            flag  = "True"
                            return render(request,'offeruploadform.html',{"error":error,"flag":flag,"Not_Show":True})
                            
                else:
                    if userobj.placement:
                        '''
                        today = datetime.datetime.today().date()                   
                        companyobj = finalresults.objects.filter(Q(enrollmentno=userid)&Q(opp_type="Placement"))
                        return render(request,'offerletterchoice.html',{"opportunities": companyobj,"date":today})
                        '''
                        error = "Please Generate NOC First"
                        flag  = "True"
                        return render(request,'offeruploadform.html',{"error":error,"flag":flag,"Not_Show":True})
                    else:
                        error = "Your have not applied for placements"
                        flag  = "True"
                        return render(request,'offeruploadform.html',{"error":error,"flag":flag,"Not_Show":True})
            else: 
                if userobj.OfferLetterVerified:
                    if userobj.OfferLetterComment is None:
                        msg = "Your have already submitted offer letter. It is verified."
                        cog = "Congratulations! for your new Job. Have a great future ahead.  Thank You"
                        flag  = "True"
                        return render(request,'offeruploadform.html',{"cog":cog,"msg":msg,"flag":flag,"Not_Show":True})
                    else:
                        error = "Your have already submitted offer letter. It as mentioned error : " + str(userobj.OfferLetterComment) + ". Please upload it once again."
                        flag  = "True"
                        try:
                            studentplacedDetailsobj = studentplacedDetails.objects.get(enrollmentno=userid)
                            studentInternshipDetailsobj = studentInternshipDetails.objects.get(enrollmentno=userid)
                            company_name =  studentplacedDetailsobj.companyname
                            job_role = studentplacedDetailsobj.typeofjob
                            package =  studentplacedDetailsobj.package
                            bond = studentplacedDetailsobj.bondterm
                            stipend = studentInternshipDetailsobj.stipend
                            encode_company = studentplacedDetailsobj.encode_company
                            return render(request,'offeruploadform.html',{"company": company_name,"stipend":stipend,"role":job_role,"package":package,"bond":bond,"opp":encode_company,"error":error,"flag":flag})   
                        except Exception as e :
                            error = str(error) + "Invalid" + str(e)
                            flag  = "True"
                            return render(request,'offeruploadform.html',{"error":error,"flag":flag})
                        
                else:                    
                    error = "Your have already submitted offer letter. It is under verification"
                    flag  = "True"
                    return render(request,'offeruploadform.html',{"error":error,"flag":flag,"Not_Show":True})
                
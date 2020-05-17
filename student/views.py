from django.shortcuts import render,redirect
from student.models import *
from opportunity.models import internshipplusplacementopportunity,internshipopportunity,placementopportunity
from django.http import HttpResponse
import psycopg2
from django.contrib.auth.models import User,auth
#from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.mail import EmailMessage
from random import seed
from random import randint
from .forms  import DetailsForm,AcademicDetailsHSCForm,CurrentAcadamicDetailsForm,PlacementDetailsForm,CompletedDetailsForm,AcademicDetailsDiplomaForm
from studentcoordinator.models import city
from django.core.files.storage import FileSystemStorage
import hashlib
from django.conf import settings
import base64
from django.db.models import Q
import shutil
import datetime
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf #created in step 4



media_root = settings.MEDIA_ROOT

class GeneratePdf(View):
    def get(request, *args, **kwargs):
        data = {
            'name': 'Harsh Patel', 
            'En': '16012121021',
            'pro':'BDA',
        }
        pdf = render_to_pdf('createpdf.html', data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "letter_%s.pdf" %("12341231")
            content = "inline; filename=%s" %(filename)
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha224(hash_string.encode()).hexdigest()
    return sha_signature

def content_file_name_resume(uid, filename, firstname):
    ext = filename.split('.')[-1]
    uid = str(uid)
    name = firstname[0] + str(uid) + firstname[len(firstname)-1]
    name = encrypt_string(name)
    filename = "%s.%s" % (name, ext)
    return "../media/" + name + '/data/resume/'+filename

def content_file_name_photo(uid, filename, firstname):
    ext = filename.split('.')[-1]
    uid = str(uid)
    name = firstname[0] + str(uid) + firstname[len(firstname)-1]
    name = encrypt_string(name)
    filename = "%s.%s" % (name, ext)
    return "../media/" + name + '/data/photo/'+filename

def content_file_name_sign(uid, filename, firstname):
    ext = filename.split('.')[-1]
    uid = str(uid)
    name = firstname[0] + str(uid) + firstname[len(firstname)-1]
    name = encrypt_string(name)
    filename = "%s.%s" % (name, ext)
    return "../media/"+ name + '/data/sign/'+filename

@login_required
def tnc(request):
    return render(request,"tnc.html")

@login_required
def applysuccessfull(request):
    return render(request,"appliedsuccessfull.html")


@login_required
def  chooseone(request):
    if request.POST:
        if request.session.has_key("uid") and request.session.get("uid")!=None: 
            userid = request.session.get("uid")
            choice = request.POST.get('internship_or_both')
            try:
                obj = completeddetails.objects.get(enrollmentno = userid)
            except completeddetails.DoesNotExist:
                obj = completeddetails.objects.create(enrollmentno = userid)
            obj.Filleddetails=False
            try:   
               obj1 = details.objects.get(enrollmentno = userid)         
            except  details.DoesNotExist:
                details.objects.create(enrollmentno = userid)         
                obj1 = details.objects.get(enrollmentno = userid)          
            if choice == "Internship":
                obj.internship=True
                obj.placement=False
            else:    
                obj.internship=True
                obj.placement=True                
            obj.save()        
            obj1.save()
            return redirect("registration")              
        else: 
            return redirect("login")
    else:    
        if request.session.has_key("uid"): 
            userid = request.session.get("uid")
            try:
                obj = completeddetails.objects.get(enrollmentno = userid)
            except completeddetails.DoesNotExist:
                obj = completeddetails.objects.create(enrollmentno = userid)
            if obj.internship or obj.placement:         
                return redirect("registration")              
            else:
                form = CompletedDetailsForm(request.POST or None)            
                context = {"form": form}  
                return render(request,"user_choice.html",context)
        else:
            return redirect("/login")

@login_required
def enterdetails(request):
    initial_data =  {}               
    form = DetailsForm(request.POST or None,initial=initial_data)            
    if request.session.has_key("uid") and request.session.get("uid")!=None: 
        userid = request.session.get("uid")
        print(userid)
        try:   
            obj = details.objects.get(enrollmentno = userid)         
        except details.DoesNotExist:
            details.objects.create(enrollmentno = userid)
            obj = details.objects.get(enrollmentno = userid)                  
        if request.POST:
            if form.is_valid():
                firstname = request.POST.get('firstname')
                middlename = request.POST.get('middlename')
                lastname = request.POST.get('lastname')
                gender = request.POST.get('gender')
                dob = request.POST.get('dob')
                phno = request.POST.get('phno')
                parentphno = request.POST.get('parentphno')
                program = request.POST.get('program')
                email = request.POST.get('email')
                hsc_or_diploma = request.POST.get('hsc_or_diploma')            
                obj.firstname =  firstname
                obj.middlename =  middlename
                obj.lastname =  lastname
                obj.gender =  gender
                obj.dob =  dob
                obj.phno =  phno
                obj.parentphno =  parentphno
                obj.program =  program
                obj.email = email
                request.session["firstname"] = firstname
                request.session["middlename"] = middlename
                request.session["lastname"] = lastname
                request.session["gender"] = gender 
                request.session["dob"] = dob
                request.session["phno"] = phno
                request.session["parentphno"] = parentphno
                request.session["program"] = program
                request.session["email"] =  email 
                request.session["hsc_or_diploma"] = hsc_or_diploma
                obj.save()
                return redirect('academic')              
        else:
            firstname=middlename=lastname=gender=dob=phno=parentphno=program=email=hsc_or_diploma= None            
            if obj.firstname is None:
                if request.session.has_key("firstname"): 
                    firstname = request.session.get("firstname")
            else:
                firstname = obj.firstname
            
            if obj.middlename is None:
                if request.session.has_key("middlename"): 
                    middlename = request.session.get("middlename") 
            else:
                middlename = obj.middlename
            
            if obj.lastname is None:  
                if request.session.has_key("lastname"):  
                    lastname = request.session.get("lastname")
            else:
                lastname = obj.lastname
            
            if obj.gender is None:
                if request.session.has_key("gender"):  
                    gender = request.session.get("gender")
            else:
                gender = obj.gender
            
            if obj.dob is None:  
                if request.session.has_key("dob"):  
                    dob = request.session.get("dob") 
            else:
                dob = obj.dob 
            
            if obj.phno is None:  
                if request.session.has_key("phno"):  
                    phno = request.session.get("phno")  
            else:        
                phno = obj.phno
            
            if obj.parentphno is None:
                if request.session.has_key("parentphno"):
                    parentphno = request.session.get("parentphno")
            else:        
                parentphno = obj.parentphno
            
            if obj.program is None: 
                if request.session.has_key("program"): 
                    program = request.session.get("program")
            else:
                program = obj.program

            if obj.email is None:   
                if request.session.has_key("email"):   
                    email = request.session.get("email")
            else:
                email = obj.email
                
            if request.session.has_key("hsc_or_diploma"):  
                hsc_or_diploma = request.session.get("hsc_or_diploma")
            initial_data =  { 'enrollmentno': userid ,
            'firstname':firstname,
            'middlename':middlename,
            'lastname':lastname,
            'gender':gender,
            'dob':dob,
            'phno':phno,
            'parentphno':parentphno,
            'program':program,
            'email':email,
            'hsc_or_diploma':hsc_or_diploma}   
            form = DetailsForm(request.POST or None,initial=initial_data)            
            context = {"form": form}       
            return render(request,"registrationform.html",context)
    else:
        return redirect('login')

@login_required
def enteracademicdetails(request):
    if request.session.has_key("uid"): 
        if request.session.has_key("firstname") and request.session.has_key("middlename") and  request.session.has_key("lastname") and  request.session.has_key("gender") and  request.session.has_key("dob") and  request.session.has_key("phno") and  request.session.has_key("parentphno") and  request.session.has_key("program") and  request.session.has_key("email") and  request.session.has_key("hsc_or_diploma"):
            userid = request.session.get("uid")
            if request.session.has_key("hsc_or_diploma"):  
                obj = details.objects.get(enrollmentno = userid)    
                hsc_or_diploma = request.session.get("hsc_or_diploma")
                if hsc_or_diploma == "HSC":
                    form = AcademicDetailsHSCForm(request.POST or None)
                else:
                    form = AcademicDetailsDiplomaForm(request.POST or None)
                
                choice = request.POST.get('submit')
                if choice == "Previous":
                    return redirect('registration')
                else:            
                    if request.POST:
                        choice = request.POST.get('submit')
                        if form.is_valid():
                            ssc_year = request.POST.get('ssc_year')
                            ssc_percentage = request.POST.get('ssc_percentage')
                            ssc_board = request.POST.get('ssc_board')
                            request.session["ssc_year"] = ssc_year
                            request.session["ssc_percentage"] = ssc_percentage
                            request.session["ssc_board"] = ssc_board                    
                            obj.ssc_year = ssc_year
                            obj.ssc_percentage = ssc_percentage
                            obj.ssc_board = ssc_board                    
                            
                            if hsc_or_diploma == "HSC":
                                hsc_year = request.POST.get('hsc_year')
                                hsc_percentage = request.POST.get('hsc_percentage')
                                hsc_board = request.POST.get('hsc_board')
                                request.session["hsc_year"] = hsc_year
                                request.session["hsc_percentage"] = hsc_percentage
                                request.session["hsc_board"] = hsc_board
                                obj.hsc_year = hsc_year
                                obj.hsc_percentage = hsc_percentage
                                obj.hsc_board = hsc_board
                                request.session["diploma_year"] = None
                                request.session["diploma_university"] = None
                                request.session["diploma_percentage"] = None
                                obj.diploma_year = None
                                obj.diploma_university = None
                                obj.diploma_percentage = None                        
                            else:
                                diploma_year = request.POST.get('diploma_year')
                                diploma_university = request.POST.get('diploma_university')
                                diploma_percentage = request.POST.get('diploma_percentage')
                                request.session["hsc_year"] = None
                                request.session["hsc_percentage"] = None
                                request.session["hsc_board"] = None
                                obj.hsc_year = None
                                obj.hsc_percentage = None
                                obj.hsc_board = None
                                request.session["diploma_year"] = diploma_year
                                request.session["diploma_university"] = diploma_university
                                request.session["diploma_percentage"] = diploma_percentage
                                obj.diploma_year = diploma_year
                                obj.diploma_university = diploma_university
                                obj.diploma_percentage = diploma_percentage
                            obj.save()                        
                            return redirect('current_academic')
                    else:
                        ssc_year = ssc_percentage = ssc_board = diploma_year = diploma_university = diploma_percentage = hsc_year = hsc_percentage = hsc_board = None
                        if obj.ssc_year is None:                 
                            if request.session.has_key("ssc_year"): 
                                ssc_year = request.session.get("ssc_year")
                        else:    
                            ssc_year = obj.ssc_year
                    
                        if obj.ssc_percentage is None:
                            if request.session.has_key("ssc_percentage"): 
                                ssc_percentage = request.session.get("ssc_percentage") 
                        else:
                            ssc_percentage = obj.ssc_percentage
                    
                        if obj.ssc_board is None:  
                            if request.session.has_key("ssc_board"):  
                                ssc_board = request.session.get("ssc_board")
                        else:    
                            ssc_board = obj.ssc_board
                    
                        if obj.diploma_year is None:  
                            if request.session.has_key("diploma_year"):  
                                diploma_year = request.session.get("diploma_year")
                        else:
                            diploma_year = obj.diploma_year
                    
                        if obj.diploma_university is None:  
                            if request.session.has_key("diploma_university"):  
                                diploma_university = request.session.get("diploma_university") 
                        else:                    
                            diploma_university = obj.diploma_university
                    
                        if obj.diploma_percentage is None:  
                            if request.session.has_key("diploma_percentage"):  
                                diploma_percentage = request.session.get("diploma_percentage")  
                        else:    
                            diploma_percentage = obj.diploma_percentage
                        
                        if obj.hsc_year is None:
                            if request.session.has_key("hsc_year"):
                                hsc_year = request.session.get("hsc_year")
                        else:        
                            hsc_year = request.session.get("hsc_year")
                        
                        if obj.hsc_percentage is None: 
                            if request.session.has_key("hsc_percentage"): 
                                hsc_percentage = request.session.get("hsc_percentage")
                        else:
                            hsc_percentage = request.session.get("hsc_percentage")
                        
                        if obj.hsc_board is None:   
                            if request.session.has_key("hsc_board"):   
                                hsc_board = request.session.get("hsc_board")                
                        else:
                            hsc_board = request.session.get("hsc_board")                
                        
                        if hsc_or_diploma == "HSC":              
                            context = {"form": form}
                            initial_data =  { 'ssc_year':  ssc_year ,
                            'ssc_percentage':ssc_percentage,
                            'ssc_board':ssc_board,
                            'hsc_year':hsc_year,
                            'hsc_percentage':hsc_percentage,
                            'hsc_board':hsc_board,
                            }
                            form = AcademicDetailsHSCForm(request.POST or None,initial=initial_data)
                        else:
                            initial_data =  { 'ssc_year':  ssc_year ,
                            'ssc_percentage': ssc_percentage,
                            'ssc_board' : ssc_board,
                            'diploma_year' : diploma_year,
                            'diploma_percentage': diploma_percentage,
                            'diploma_university':diploma_university,
                            }
                            form = AcademicDetailsDiplomaForm(request.POST or None,initial=initial_data)
                        context = {"form": form }
                        return render(request,"academicdetailsform.html",context)
            else:
                return redirect('registration')
        else:
            return redirect('registration')
    else:
        return redirect('login')

@login_required
def entercurrentacademicdetails(request):
    if request.session.has_key("uid"):
        if request.session.has_key("ssc_year") and request.session.has_key("ssc_percentage")  and request.session.has_key("ssc_board")  and ( (request.session.has_key("diploma_year")  and request.session.has_key("diploma_university")  and request.session.has_key("diploma_percentage") )  or ( request.session.has_key("hsc_year")  and request.session.has_key("hsc_percentage")  and request.session.has_key("hsc_board") ) ):                   
            form = CurrentAcadamicDetailsForm(request.POST or None)
            userid = request.session.get("uid")
            obj = details.objects.get(enrollmentno = userid)    
            choice = request.POST.get('submit')
            if choice == "Previous":
                return redirect('academic')
            if request.POST:
                if form.is_valid():
                    sgpa_sem_1 =  request.POST.get('sgpa_sem_1')
                    sgpa_sem_2 =  request.POST.get('sgpa_sem_2')
                    sgpa_sem_3 =  request.POST.get('sgpa_sem_3')
                    sgpa_sem_4 =  request.POST.get('sgpa_sem_4')
                    sgpa_sem_5 =  request.POST.get('sgpa_sem_5')
                    sgpa_sem_6 =  request.POST.get('sgpa_sem_6')
                    sgpa_sem_7 =  request.POST.get('sgpa_sem_7')
                    #sgpa_sem_8 =  request.POST.get('sgpa_sem_8')
                    cgpa =  request.POST.get('cgpa')
                    effbacklog = request.POST.get('effbacklog')
                    obj.sgpa_sem_1 =  sgpa_sem_1
                    obj.sgpa_sem_2 =  sgpa_sem_2
                    obj.sgpa_sem_3 =  sgpa_sem_3
                    obj.sgpa_sem_4 =  sgpa_sem_4
                    obj.sgpa_sem_5 =  sgpa_sem_5
                    obj.sgpa_sem_6 =  sgpa_sem_6
                    obj.sgpa_sem_7 =  sgpa_sem_7
                    #obj.sgpa_sem_8 =  sgpa_sem_8
                    obj.cgpa =  cgpa
                    obj.effbacklog  = effbacklog                  
                    request.session["sgpa_sem_1"] =  sgpa_sem_1
                    request.session["sgpa_sem_2"] =  sgpa_sem_2
                    request.session["sgpa_sem_3"] =  sgpa_sem_3
                    request.session["sgpa_sem_4"] =  sgpa_sem_4
                    request.session["sgpa_sem_5"] =  sgpa_sem_5
                    request.session["sgpa_sem_6"] =  sgpa_sem_6
                    request.session["sgpa_sem_7"] =  sgpa_sem_7
                    #request.session["sgpa_sem_8"] =  sgpa_sem_8
                    request.session["cgpa"] =  cgpa
                    request.session["effbacklog"] = effbacklog  
                    obj.save()
                    return redirect('placement_reg')
            else:
                sgpa_sem_1 = sgpa_sem_2 = sgpa_sem_3 = sgpa_sem_4 = sgpa_sem_5 = sgpa_sem_6 = sgpa_sem_7 =  sgpa_sem_8 = cgpa = effbacklog = None            
                
                if obj.sgpa_sem_1 is None:
                    if request.session.has_key("sgpa_sem_1"):
                        sgpa_sem_1 = request.session.get("sgpa_sem_1")
                else:
                    sgpa_sem_1 = obj.sgpa_sem_1

                if obj.sgpa_sem_2 is None:
                    if request.session.has_key("sgpa_sem_2"): 
                        sgpa_sem_2 = request.session.get("sgpa_sem_2")
                else:    
                    sgpa_sem_2 = obj.sgpa_sem_2
                
                if obj.sgpa_sem_3 is None: 
                    if request.session.has_key("sgpa_sem_3"): 
                        sgpa_sem_3 = request.session.get("sgpa_sem_3")
                else:    
                    sgpa_sem_3 = obj.sgpa_sem_3
                
                if obj.sgpa_sem_4 is None:
                    if request.session.has_key("sgpa_sem_4"):
                        sgpa_sem_4 = request.session.get("sgpa_sem_4")
                else:   
                    sgpa_sem_4 = obj.sgpa_sem_4
                
                if obj.sgpa_sem_5 is None:
                    if request.session.has_key("sgpa_sem_5"):
                        sgpa_sem_5 = request.session.get("sgpa_sem_5")
                else:    
                    sgpa_sem_5 = obj.sgpa_sem_5
                
                if obj.sgpa_sem_6 is None:
                    if request.session.has_key("sgpa_sem_6"): 
                        sgpa_sem_6 = request.session.get("sgpa_sem_6")
                else:    
                    sgpa_sem_6 = obj.sgpa_sem_6
                
                if obj.sgpa_sem_7 is None:
                    if request.session.has_key("sgpa_sem_7"): 
                        sgpa_sem_7 = request.session.get("sgpa_sem_7")
                else:    
                    sgpa_sem_7 = obj.sgpa_sem_7

                # if obj.sgpa_sem_8 is None:
                #     if request.session.has_key("sgpa_sem_8"): 
                #         sgpa_sem_8 = request.session.get("sgpa_sem_8")
                # else:
                #     sgpa_sem_8 = obj.sgpa_sem_8

                if obj.cgpa is None:
                    if request.session.has_key("cgpa"):
                        cgpa = request.session.get("cgpa")
                else:    
                    cgpa = obj.cgpa
                
                if obj.effbacklog is None:
                    if request.session.has_key("effbacklog"):
                        effbacklog = request.session.get("effbacklog")
                else:        
                    effbacklog = obj.effbacklog
                    
                initial_data =  { 'sgpa_sem_1'  :  sgpa_sem_1,
                    'sgpa_sem_2'  :  sgpa_sem_2 ,
                    'sgpa_sem_3'  :  sgpa_sem_3 ,
                    'sgpa_sem_4'  :  sgpa_sem_4 ,
                    'sgpa_sem_5'  :  sgpa_sem_5 ,
                    'sgpa_sem_6'  :  sgpa_sem_6 ,
                    'sgpa_sem_7'  :  sgpa_sem_7 ,
                    'sgpa_sem_8'  :  sgpa_sem_8 ,
                    'cgpa' : cgpa ,
                    'effbacklog' : effbacklog 
                    }
                form = CurrentAcadamicDetailsForm(request.POST or None,initial=initial_data)
                context = {"form": form }        
                return render(request,"CurrentAcadamicDetailsForm.html",context)
        else:
            return redirect('academic')
    else:
        return redirect('login')

@login_required
def enterplacementdetails(request):
    if request.session.has_key("uid"): 
        if request.session.has_key("sgpa_sem_1") and request.session.has_key("sgpa_sem_2") and request.session.has_key("sgpa_sem_3") and request.session.has_key("sgpa_sem_4") and request.session.has_key("sgpa_sem_5") and request.session.has_key("sgpa_sem_6") and request.session.has_key("sgpa_sem_7") and request.session.has_key("sgpa_sem_8") and request.session.has_key("cgpa") and request.session.has_key("effbacklog"): 
            userid = request.session.get("uid")
            form = PlacementDetailsForm(request.POST or None,request.FILES)
            choice = request.POST.get('submit')
            obj = details.objects.get(enrollmentno = userid)    
            obj1 = completeddetails.objects.get(enrollmentno=userid)
            if choice == "Previous":
                return redirect('current_academic')
            else:
                if request.POST:
                    if form.is_valid():
                        skillset = request.POST.get('skillset')
                        cityofinterest =  request.POST.get('cityofinterest')
                        positionofinterest = request.POST.get('positionofinterest')
                        toolsandtechnology = request.POST.get('toolsandtechnology')
                        linkedinURL = request.POST.get('linkedinURL')
                       
                        photo = request.FILES['photo']
                        resume = request.FILES['resume']
                        sign = request.FILES['sign']
                        
                        ext_photo = photo.name.split('.')[-1]
                        ext_resume = resume.name.split('.')[-1]
                        ext_sign = sign.name.split('.')[-1]
                        
                        sha224_uid = encrypt_string(str(userid))
                        
                        user_name = str(sha224_uid)
                        
                        filename_photo = "%s.%s" % (user_name, ext_photo)
                        filename_resume = "%s.%s" % (user_name, ext_resume)
                        filename_sign = "%s.%s" % (user_name, ext_sign)
                        
                        dir_path = "/Users/rajrao/Desktop/tnp-New-Latest/trainingandplacement/media"
                        doc_path = "/documents/"
                        img_path = "/userphotos/"
                        sign_path = "/usersign/"

                        with open(dir_path + doc_path + filename_resume,'wb') as f:
                            shutil.copyfileobj(resume,f)
                        
                        with open(dir_path + img_path + filename_photo,'wb') as f:
                            shutil.copyfileobj(photo,f)
                        
                        with open(dir_path + sign_path + filename_sign,'wb') as f:
                            shutil.copyfileobj(sign,f)
                        
                        obj.skillset = skillset
                        obj.cityofinterest =  cityofinterest
                        obj.positionofinterest = positionofinterest
                        obj.toolsandtechnology = toolsandtechnology
                        obj.photo = dir_path + img_path + filename_photo
                        obj.resume = dir_path + doc_path + filename_resume
                        obj.linkedinURL = linkedinURL
                        obj.sign = dir_path + sign_path + filename_sign
                        
                        request.session["skillset"] = skillset
                        request.session["cityofinterest"] =  cityofinterest
                        request.session["positionofinterest"] = positionofinterest
                        request.session["toolsandtechnology"] = toolsandtechnology
                        request.session["linkedinURL"] = linkedinURL
                        obj.save()                        
                        obj1.filleddetails=True
                        obj1.save()
                        return redirect('student')
                        
                else:        
                    skillset = cityofinterest = positionofinterest = toolsandtechnology = linkedinURL = None
                    if obj.skillset is None:
                        if request.session.has_key("skillset"):
                            skillset = request.session.get("skillset") 
                    else:     
                        skillset =  obj.skillset
                        
                    if obj.cityofinterest is None:
                        if request.session.has_key("cityofinterest"):
                            skillset = request.session.get("cityofinterest") 
                    else:     
                        cityofinterest =  obj.cityofinterest
                    
                    if obj.positionofinterest is None:
                        if request.session.has_key("positionofinterest"):
                            positionofinterest = request.session.get("positionofinterest") 
                    else:     
                        positionofinterest =  obj.positionofinterest
                    
                    if obj.toolsandtechnology is None:
                        if request.session.has_key("toolsandtechnology"):
                            toolsandtechnology = request.session.get("toolsandtechnology") 
                    else:     
                        toolsandtechnology =  obj.toolsandtechnology
                    
                    if obj.linkedinURL is None:
                        if request.session.has_key("linkedinURL"):
                            linkedinURL = request.session.get("linkedinURL") 
                    else:     
                        linkedinURL =  obj.linkedinURL                  
                    
                    cities = city.objects.all()    
                    allposition = position.objects.all()
                    initial_data =  { 'skillset' : skillset,
                        'cityofinterest' :   cityofinterest,
                        'positionofinterest' :  positionofinterest,
                        'toolsandtechnology' : toolsandtechnology,
                        'linkedinURL' :  linkedinURL,
                        }
                    form = PlacementDetailsForm(request.POST or None,initial=initial_data)
                    context = {"form": form,"cities":cities,"allposition":allposition}
                    return render(request,"placementdetailsform.html",context)
        else:
            return redirect('current_academic')
    else:
        return redirect('login')

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
def enterplacementdetails(request):
    if request.session.has_key("uid"): 
        userid = request.session.get("uid")
        form = PlacementDetailsForm(request.POST or None,request.FILES)
        choice = request.POST.get('submit')
        obj = details.objects.get(enrollmentno = userid)    
        obj1 = completeddetails.objects.get(enrollmentno=userid)
        if choice == "Previous":
            return redirect('current_academic')
        else:
            if request.POST:
                try:
                    skillset = request.POST.get('skillset')
                    cityofinterest =  request.POST.get('cityofinterest')
                    positionofinterest = request.POST.get('positionofinterest')
                    toolsandtechnology = request.POST.get('toolsandtechnology')
                    linkedinURL = request.POST.get('linkedinURL')

                    
                    photo = request.FILES['photo']
                    resume = request.FILES['resume']
                    sign = request.FILES['sign']
                    
                    ext_photo = photo.name.split('.')[-1]
                    ext_resume = resume.name.split('.')[-1]
                    ext_sign = sign.name.split('.')[-1]
                    
                    sha224_uid = encrypt_string(str(userid))
                    
                    user_name = str(sha224_uid)
                    
                    filename_photo = "%s.%s" % (user_name, ext_photo)
                    filename_resume = "%s.%s" % (user_name, ext_resume)
                    filename_sign = "%s.%s" % (user_name, ext_sign)
                    
                    dir_path = "/Users/rajrao/Desktop/trainingandplacement-master/media"
                    doc_path = "/documents/"
                    img_path = "/userphotos/"
                    sign_path = "/usersign/"

                    with open(dir_path + doc_path + filename_resume,'wb') as f:
                        shutil.copyfileobj(resume,f)
                    
                    with open(dir_path + img_path + filename_photo,'wb') as f:
                        shutil.copyfileobj(photo,f)
                    
                    with open(dir_path + sign_path + filename_sign,'wb') as f:
                        shutil.copyfileobj(sign,f)
                    
                    obj.skillset = skillset
                    obj.cityofinterest =  cityofinterest
                    obj.positionofinterest = positionofinterest
                    obj.toolsandtechnology = toolsandtechnology
                    obj.photo = dir_path + img_path + filename_photo
                    obj.resume = dir_path + doc_path + filename_resume
                    obj.linkedinURL = linkedinURL
                    obj.sign = dir_path + sign_path + filename_sign
                    
                    request.session["skillset"] = skillset
                    request.session["cityofinterest"] =  cityofinterest
                    request.session["positionofinterest"] = positionofinterest
                    request.session["toolsandtechnology"] = toolsandtechnology
                    request.session["linkedinURL"] = linkedinURL
                    obj.save()                        
                    obj1.filleddetails=True
                    obj1.save()
                    return redirect('login')
                except Exception as e:
                    return HttpResponse("<html><body><br/>"+e+"<br/></body></html>")
            else:        
                skillset = cityofinterest = positionofinterest = toolsandtechnology = linkedinURL = None
                if obj.skillset is None:
                    if request.session.has_key("skillset"):
                        skillset = request.session.get("skillset") 
                else:     
                    skillset =  obj.skillset
                    
                if obj.cityofinterest is None:
                    if request.session.has_key("cityofinterest"):
                        skillset = request.session.get("cityofinterest") 
                else:     
                    cityofinterest =  obj.cityofinterest
                
                if obj.positionofinterest is None:
                    if request.session.has_key("positionofinterest"):
                        positionofinterest = request.session.get("positionofinterest") 
                else:     
                    positionofinterest =  obj.positionofinterest
                
                if obj.toolsandtechnology is None:
                    if request.session.has_key("toolsandtechnology"):
                        toolsandtechnology = request.session.get("toolsandtechnology") 
                else:     
                    toolsandtechnology =  obj.toolsandtechnology
                
                if obj.linkedinURL is None:
                    if request.session.has_key("linkedinURL"):
                        linkedinURL = request.session.get("linkedinURL") 
                else:     
                    linkedinURL =  obj.linkedinURL                  
                
                cities = city.objects.all()    
                allposition = position.objects.all()
                initial_data =  { 'skillset' : skillset,
                    'cityofinterest' :   cityofinterest,
                    'positionofinterest' :  positionofinterest,
                    'toolsandtechnology' : toolsandtechnology,
                    'linkedinURL' :  linkedinURL,
                    }
                form = PlacementDetailsForm(request.POST or None,initial=initial_data)
                context = {"form": form,"cities":cities,"allposition":allposition}
                return render(request,"placementdetailsform.html",context)
    else:
        return redirect('login')
# Create your views here

@login_required
def dashboard(request):
    if request.method == 'POST':
        userid = request.session.get("uid")
        print(request.POST['otp'])
        print(request.session.get('OTP'))
        if (str(request.POST['otp']) == str(request.session.get('OTP'))):
            obj = User.objects.get(username=userid)
            obj.set_password(request.POST['pass'])
            obj.save()
            del request.session['firstlogin']
            del request.session['email']
            return redirect('/passwordchangesuccessfull')              
        else:
            return render(request,'changepassword.html',{"message":"OTP Mismatch"})    
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

@login_required
def allowchangepassword(request):
    if request.method == 'POST':
        userid = request.session.get("uid")
        print(request.POST['otp'])
        print(request.session.get('OTP'))
        if (str(request.POST['otp']) == str(request.session.get('OTP'))):
            obj = User.objects.get(username=userid)
            obj.set_password(request.POST['pass'])
            obj.save()
            if request.session.has_key('firstlogin'):
                del request.session['firstlogin']
            if request.session.has_key('email'):
                del request.session['email']
            request.session["message"]="Password Change Successfull"
            return redirect('/login')              

        else:
            try:    
                otp = randint(10000, 99999)
                print(otp)
                request.session["OTP"] = otp
                email = EmailMessage('OTP', 'Your OTP for password change is :- '+str(otp), to=[str(request.session.get("email"))])
                print(email.send())
                return render(request,'forgotpassword2.html',{"message":"OTP Mismatch"})	                                       
            except Exception as e: 
                print(e)
                return render(request,'forgotpassword2.html',{"message":"OTP Mismatch"+str(e)})	                                       
    else:
        try:    
            #seed(100)
            otp = randint(10000, 99999)
            print(otp)
            request.session["OTP"] = otp
            email = EmailMessage('OTP', 'Your OTP for password change is :- '+str(otp), to=[str(request.session.get("email"))])
            print(email.send())
        except Exception as e: 
            print(e)
            return render(request,'forgotpassword2.html',{"message":e})	                                       
        return render(request,'forgotpassword2.html')	
  
@login_required
def changepassword(request):
    if request.POST:
        password = request.POST['password']
        userid = request.session.get("uid")
        user = auth.authenticate(username=userid, password=password)
        if user is None: 
                return render(request,'enterpassword.html',{"message":"Wrong Credentials"})     
        try:    
            obj = User.objects.get(username=userid)
            otp = randint(10000, 99999)
            emailid = obj.email
            request.session["email"]=emailid
            request.session["OTP"] = otp
            email = EmailMessage('OTP', 'Your OTP for password change is :- '+str(otp), to=[emailid])
            email.send()
            return redirect("auth_complete")
        except Exception as e: 
            return render(request,'enterpassword.html',{"message":"Check your internet connection"})            
    else:
        return render(request,'enterpassword.html') 

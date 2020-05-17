from django.shortcuts import render,redirect
from student.models import details
from faculty.models import fdetails
from django.http import HttpResponse
import psycopg2
from django.contrib.auth.models import User,auth
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.mail import EmailMessage
from random import seed
from random import randint
from django.utils.datastructures import MultiValueDictKeyError



def passwordchangesuccessfull(request):
    try:
        print("Executed")
        auth.logout(request)
        if request.session.has_key('uid'):
            del request.session['uid']
        if request.session.has_key('username'):
            del request.session['username']
        if request.session.has_key('isstaff'):
            del request.session["isstaff"]
        if request.session.has_key('firstlogin'):
            del request.session['firstlogin']
        if request.session.has_key('email'):
            del request.session['email']
    except KeyError:
        pass
    return render(request,'passwordchangesuccessfull.html')	        
            
def userlogout(request):
    try:
        print("Executed")
        auth.logout(request)
        if request.session.has_key('uid'):
            del request.session['uid']
        if request.session.has_key('username'):
            del request.session['username']
        if request.session.has_key('isstaff'):
            del request.session["isstaff"]
        if request.session.has_key('firstlogin'):
            del request.session['firstlogin']
        if request.session.has_key('email'):
            del request.session['email']
    except KeyError:
        pass
    return redirect('login')	        


@csrf_protect
@never_cache
def login_(request):
    if request.method == 'POST':
        if str(request.POST['submitbutton'])=="Login":
            userid = request.POST['userid']
            password = request.POST['password']
            user = auth.authenticate(username=userid, password=password)
            print(user)
            if user is None: 
                return render(request,'login.html',{"message":"Wrong Credentials"})	
            else:
                request.session["uid"] = userid   
                auth.login(request,user)
                if password == "4321":
                    request.session["firstlogin"]= "True"
                    request.session["email"]= user.email
                if(len(userid)==6):
                    return redirect('faculty')            
                elif(len(userid)==11):
                    request.session["isstaff"] = user.is_staff
                    if user.is_staff:
                        return redirect('studentcoordinator')  
                    else:
                        return redirect('student')      
                elif(len(userid)==5):
                    return redirect("admin")
                else:
                    return render(request,'login.html',{"message":"Wrong Credentials"})	
        else:
            return redirect('forgotpassword')      
    else:
        try:
            if request.GET['submitbutton']=="Forgot-Password?":
                return redirect('forgotpassword')      
        except MultiValueDictKeyError:
            pass
        if request.session.has_key("uid"):
            if len(request.session.get("uid"))==11:
                if request.session.get("isstaff"):
                    return redirect('studentcoordinator')  
                else:    
                    return redirect('student')  
            elif len(request.session.get("uid"))==6:
                return redirect('faculty') 
        try:
            if request.session.has_key('username'):
                del request.session['username']
            if request.session.has_key('isstaff'):
                del request.session["isstaff"]
            if request.session.has_key('firstlogin'):
                del request.session['firstlogin']
            if request.session.has_key('email'):
                del request.session['email']
        except KeyError:
            pass
        msg=""
        if request.session.has_key("message"):
            msg = request.session.get("message")
            del request.session['message']
            print(msg)
        return render(request,'login.html',{"message":msg})	
    
def changepassword(request):
    if request.method == 'POST':
        userid = request.session.get("uid")
        detaildata = details.objects.get(enrollmentno=userid)
        if (str(request.POST['otp']) == str(request.session.get('OTP'))):
            obj = User.objects.get(username=userid)
            obj.set_password(request.POST['pass'])
            obj.save()
            if request.session.has_key('firstlogin'):
                del request.session['firstlogin']
            if request.session.has_key('email'):
                del request.session['email']
            request.session["message"]="Password Change Successfull"    
            del request.session['uid']
            return redirect('/login')              
        else:
            return render(request,'forgotpassword2.html',{"message":"OTP Mismatch"})	                                       
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

def forgotpassword(request):
    if request.method == 'POST':
        userid = request.POST['userid']
        emailid = request.POST['emailid']
        print(userid)
        print(emailid)
        obj = User.objects.get(username=userid)
        print(obj.email)
        if str(emailid) == str(obj.email):
            try:    
                #seed(100)
                otp = randint(10000, 99999)
                print(otp)
                request.session["OTP"] = otp
                request.session["email"] = str(emailid)
                email = EmailMessage('OTP', 'Your OTP for password change is :- '+str(otp), to=[emailid])
                email.send()
                request.session["uid"] = userid          
                return redirect('changepassword_forgot')      
            except Exception as e: 
                print(e)
                return render(request,'forgotpassword.html',{"message":e})	                                     
        else:
            return render(request,'forgotpassword.html',{"message":"Wrong Email or User Id"})	                                 
    else: 
        try:
            if request.GET['submitbutton']=="Nevermind":
                return redirect('/')      
        except MultiValueDictKeyError:
            pass   
        return render(request,'forgotpassword.html')	                            

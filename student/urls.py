from django.urls import path,include 
from django.contrib import admin
from django.views.generic import TemplateView

from . import views


urlpatterns = [
   path('',views.dashboard, name = 'student'),
   path('showpassedopportunity',views.showpassedopportunity, name = 'showpassedopportunity'),
   path('viewprofile',views.viewprofile,name='viewprofile'),
   path('resendotp',views.dashboard,name='resendotp'),
   path('changepassword',views.changepassword,name = 'changepassword'),
   path('generate',views.GeneratePdf.get,name='pdfsave'),
   path('auth_complete',views.allowchangepassword,name='auth_complete'),
   path('registration',views.enterdetails,name='registration'),
   path('academic',views.enteracademicdetails,name='academic'),
   path('current_academic',views.entercurrentacademicdetails,name='current_academic'),
   path('placement_reg',views.enterplacementdetails,name='placement_reg'),
   path('choose',views.chooseone,name='choose'),
   path('tnc',views.tnc,name='tnc'),
   #path('<str:opportunity>',views.takeopportunity,name = 'takeopportunity'),
   path('applysuccessfull',views.applysuccessfull,name = 'applysuccessfull'),
   
]
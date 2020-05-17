from django.urls import path,include 
from django.contrib import admin
from django.views.generic import TemplateView

from . import views


urlpatterns = [
   path('',views.dashboard, name = 'studentcoordinator'),
   path('uploadothersofferletter',views.uploadothersofferletter,name = 'uploadothersofferletter'),
   path('showpassedopportunity',views.showpassedopportunity, name = 'showpassedopportunity'),
   path('internshipplusplacement',views.internshipplusplacement, name = 'internshipplusplacement'),
   path('placement',views.placement, name = 'placement'),
   path('showplacement',views.showplacement, name = 'showplacement'),
   path('viewprofile',views.viewprofile,name='viewprofile'),
   path('internship',views.internship, name = 'internship'),
   path('showinternship',views.showinternship, name = 'showinternship'),
   path('resendotp',views.dashboard,name='resendotp'),
   path('declareresult',views.declareresult,name='declareresult'),
   path('vol',views.vol,name = 'vol'),
   path('<str:opportunity>',views.declareopportunityresult,name = 'declareopportunityresult'),
   path('openofferletter/<str:student>',views.openofferletter,name = 'openofferletter'),
]
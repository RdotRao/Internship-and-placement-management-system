from django.urls import path,include 
from django.contrib import admin
from django.views.generic import TemplateView
from . import views

#path('uploadofferletter_/<str:opportunity>',views.uploadofferletter_,name = 'uploadofferletter_'),
   
urlpatterns = [
   path('showpassedopportunity',views.showpassedopportunity,name='showpassedopportunity'),
   path('openNOC',views.openNOC,name = 'openNOC'),
   path('openOL',views.openOL,name = 'openOL'),
   path('viewprofile',views.viewprofile,name='viewprofile'),
   path('uploadofferletter',views.uploadofferletter,name='uploadofferletter'),
   path('takeopportunity/<str:opportunity>',views.takeopportunity,name = 'takeopportunity'),
   path('generateNOC',views.generateNOC, name = 'generateNOC'),
   path('generateNOC_Next/<str:opportunity>',views.generateNOC_Next,name = 'generateNOC_Next'),
   path('generateNOC_final/<str:opportunity>',views.generateNOC_final,name = 'generateNOC_final'),
   path('seeopportunityresult/<str:opportunity>',views.seeopportunityresult,name = 'seeopportunityresult'),
   path('seedetailopportunityresult/<str:resulttype>',views.seedetailopportunityresult,name = 'seedetailopportunityresult'),
   path('downloadapplied/<str:opportunity>',views.downloadapplied,name = 'downloadapplied'),
   path('Applied',views.Applied,name = 'Applied'),
   path('showresult',views.showresult,name = 'showresult'),
]
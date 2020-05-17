from django.urls import path,include 
from django.contrib import admin
from django.views.generic import TemplateView

from . import views


urlpatterns = [
   path('',views.dashboard, name = 'faculty'),
   path('uploadothersofferletter',views.uploadothersofferletter,name = 'uploadothersofferletter'),
   path('vol',views.vol,name = 'vol'),
   path('internshipplusplacementfac',views.internshipplusplacement, name = 'internshipplusplacement'),
   path('placementfac',views.placement, name = 'placement'),
   path('internshipfac',views.internship, name = 'internship'),

]
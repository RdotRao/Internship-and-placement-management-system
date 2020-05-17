from django.urls import path,include 
from django.contrib import admin
from django.views.generic import TemplateView
from . import views


urlpatterns = [
   path('',views.login_, name = 'login'),
   path('login',views.login_, name = 'login'),
   path('userlogout',views.userlogout, name = 'logout'),
   #path('admin',views.login_,name='admin'),
   path('admin', admin.site.urls),
   path('forgotpassword',views.forgotpassword,name = 'forgotpassword'),
   path('changepassword_forgot',views.changepassword,name = 'changepassword_forgot'),
   path('passwordchangesuccessfull',views.passwordchangesuccessfull, name = 'passwordchangesuccessfull'),
]
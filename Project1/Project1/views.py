from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
from . import models
import time
from . import emailAPI

dt=time.asctime()
curl=settings.CURRENT_URL

#middleware to check session for main app routes
#middleware to check session for main app routes
def sessioncheck_middleware(get_response):
	def middleware(request):
		if request.path=='/login/':
			request.session['sunm']=None
			request.session['srole']=None
			response=get_response(request)
		else:
			response=get_response(request)            
		return response
	return middleware

    
def home(request):
    #return HttpResponse("<h2>Welcome to the Home page<h2>")
    return render(request,'home.html',{'curl':curl})

def about(request):
    return render(request,'about.html',{'curl':curl})

def contact(request):
    return render(request,'contact.html',{'curl':curl})

def register(request):
    if request.method=="GET":
        return render(request,'register.html',{'curl':curl})
    else:
        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")

        p = models.Register(name=name,username=email,password=password,mobile=mobile,address=address,city=city,gender=gender,status=0,role="user",dt=dt)
        p.save()

        emailAPI.sendEmail(email,password)

        return render(request,'register.html',{'msg':'User Registered Successfully','curl':curl})

def service(request):
    return render(request,'service.html',{'curl':curl})

def login(request):
    if request.method=='GET':
        return render(request,'login.html',{'curl':curl})
    else:
        email =request.POST.get("email")
        password  =request.POST.get("password")
        
        userDetails=models.Register.objects.filter(username=email,password=password,status=1)

        if len(userDetails)>0:

            # It is an configuration to store userdetails in session.
            request.session['sunm']=userDetails[0].username #request is an object and session is a property of that object, it will accept the value in key:value format.
            request.session['srole']=userDetails[0].role
            
            if userDetails[0].role=='user': #"sunm" is by default the name of the session variable.This is golabal variable,accessibly globally.
                return redirect('/user/')
            else:
                return redirect('/myadmin/')
        else:
            return render(request,'login.html',{'msg':'Invalid user, please try again','curl':curl})
                              # left hand side par kis se match karna hai and right hand side par kisko match karna hai
                                         #models refer to the module, Register is the class. 
                                         #object gives result in object form,filter used to filter data according to our choice.
                                         #In filter keyword argument will come.  
        return render(request,'login.html',{'msg':'Form Submitted','curl':curl})
from django.shortcuts import render,redirect
from django.http import HttpResponse
from Project1 import models as myapp_model
from django.core.files.storage import FileSystemStorage
from . import models


from django.conf import settings
from . import models
import time

# Middleware function to apply user checking at admin panel.

def sessioncheckmyadmin_middleware(get_response):
    def middleware(request):
        if request.path=='/myadmin/' or request.path=='/myadmin/manageusers/' or request.path=='/myadmin/manageuserstatus/' or request.path=='/myadmin/addcategory/' or request.path=='/myadmin/addsubcategory/' or request.path=='/myadmin/changepassword_admin/':
            if request.session['sunm']==None or request.session['srole']!='admin':
                response=redirect('/login/')
            else:
                response=get_response(request)
        else:
            response=get_response(request)
        return response
    return middleware

def adminhome(request):
    return render(request,"adminhome.html",{"sunm":request.session['sunm']})

def manageusers(request):
    userDetails= myapp_model.Register.objects.filter(role="user")
    return render(request,"manageusers.html",{"userDetails":userDetails,"sunm":request.session['sunm']})

def manageuserstatus(request):
    status=request.GET.get("status")
    regid=request.GET.get("regid")
    if status=="block":
        myapp_model.Register.objects.filter(regid=regid).update(status=0)
    elif status=="verify":
        myapp_model.Register.objects.filter(regid=regid).update(status=1)
    else:
        myapp_model.Register.objects.filter(regid=regid).delete()
    return redirect("/myadmin/manageusers/")

def addcategory(request):
    if request.method=="GET":
        return render(request,"addcategory.html",{"msg":"","sunm":request.session['sunm']})
    else:
        catnm=request.POST.get("catnm") #catnm is the name of the category
        caticon=request.FILES["caticon"]    #Files is used to manage the files content, it is a sort of dictionary.
        fs=FileSystemStorage()
        caticonnm=fs.save(caticon.name,caticon) #caticonnm is the name of the category icon
        p=models.Category(catnm=catnm,caticonnm=caticonnm)
        p.save()
        return render(request,"addcategory.html",{"msg":"Category added successfully.....","sunm":request.session['sunm']})

def addsubcategory(request):
    clist=models.Category.objects.all()
    if request.method=="GET":
        return render(request,"addsubcategory.html",{"msg":"","clist":clist,"sunm":request.session['sunm']})
    else:
        catnm=request.POST.get("catnm") #catnm is the name of the category
        subcatnm=request.POST.get("subcatnm")
        subcat_list=models.Subcategory.objects.filter(subcatnm=subcatnm)
        if len(subcat_list)>0:
            return render(request,"addsubcategory.html",{"msg":"Category already exist!!!","clist":clist,"sunm":request.session['sunm']})
        else:
            caticon=request.FILES["caticon"]    #Files is used to manage the files content, it is a sort of dictionary.
            print(catnm,subcatnm,caticon)
            fs=FileSystemStorage()
            subcaticonnm=fs.save(caticon.name,caticon) #caticonnm is the name of the category icon
            p=models.Subcategory(catnm=catnm,subcatnm=subcatnm,subcaticonnm=subcaticonnm)
            p.save()
            return render(request,"addsubcategory.html",{"msg":"Subcategory added successfully.....","clist":clist,"sunm":request.session['sunm']})

def changepassword(request):
    if request.method=="GET":
        return render(request,"changepassword_admin.html",{"sunm":request.session['sunm']})
    else:
        password=request.POST("password")
        adminDetails=model.Register.objects.filter(password=password,status=1)
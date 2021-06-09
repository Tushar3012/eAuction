from django.shortcuts import render,redirect
from django.http import HttpResponse
from myadmin import models as myadmin_model
from django.conf import settings
from Project1 import models as myapp_model
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import time
from . import models
media_url=settings.MEDIA_URL

# Create your views here.
# Middleware function to apply user checking at admin panel.

def sessioncheckuser_middleware(get_response):
    def middleware(request):
        if request.path=='/user/' or request.path=='/user/viewproducts/' or request.path=='/user/subcatviewproducts/' or request.path=='/user/addproducts/' or request.path=='/user/showSubcategory/' or request.path=='/user/changepassword/':
            if request.session['sunm']==None or request.session['srole']!='user':
                response=redirect('/login/')
            else:
                response=get_response(request)
        else:
            response=get_response(request)
        return response
    return middleware

def userhome(request):
    print(request.session==["sunm"])
    return render(request,"userhome.html",{"sunm":request.session['sunm']})

def viewproducts(request):
    clist=myadmin_model.Category.objects.all()
    return render(request,"viewproducts.html",{"media_url":media_url,"clist":clist,"sunm":request.session['sunm']})

def subcatviewproducts(request):
    catnm=request.GET.get("catnm")
    sclist=myadmin_model.Subcategory.objects.filter(catnm=catnm)
    return render(request,"subcatviewproducts.html",{"media_url":media_url,"sclist":sclist,"catnm":catnm,"sunm":request.session['sunm']})

def changepassworduser(request):
    if request.method=="GET":
        return render(request,"changepassworduser.html",{"sunm":request.session["sunm"],"msg":""})
    else:
        opass=request.POST.get("opass")
        npass=request.POST.get("npass")
        cnpass=request.POST.get("cnpass")
        
        userDetails=myapp_model.Register.objects.filter(username=request.session["sunm"],password=opass)
    if len(userDetails)>0:
        if npass==cnpass:
            myapp_model.Register.objects.filter(username=request.session['sunm']).update(password=cnpass)
            msg="Password Changed Successfully.Please Login again"

        else:
            msg="New & Confirm Password not matched"
    
    else:
        msg="Invalid old Password, try again"
    return render(request,"changepassworduser.html",{"sunm":request.session["sunm"],"msg":msg})

def addproducts(request):
    clist=myadmin_model.Category.objects.all()
    if request.method=="GET":
        return	render(request,"addproducts.html",{"clist":clist,"sunm":request.session['sunm'],"msg":""})
    else:
        title=request.POST.get("title")
        catnm=request.POST.get("catnm")
        subcatnm=request.POST.get("subcatnm")
        baseprice=request.POST.get("baseprice")
        description=request.POST.get("description")
        
        file1=request.FILES['file1']
        fs=FileSystemStorage()
        file1_nm=fs.save(file1.name,file1)
        if request.POST.get('file2')==None:
            file2=request.FILES['file2']        
            fs=FileSystemStorage()
            file2_nm=fs.save(file2.name,file2)
        else:
            file2_nm="eAuction.jpg"
            
        if request.POST.get('file3')==None:
            file3=request.FILES['file3']        
            fs=FileSystemStorage()
            file3_nm=fs.save(file3.name,file3)
        else:
            file3_nm="eAuction.jpg"
            
        if request.POST.get('file4')==None:
            file4=request.FILES['file4']        
            fs=FileSystemStorage()
            file4_nm=fs.save(file4.name,file4)
        else:
            file4_nm="eAuction.jpg"                
        uid=request.session['sunm']
        bstatus=0 #bs=bidding status
        dt=time.time()

        p=models.Products(title=title,catnm=catnm,subcatnm=subcatnm,baseprice=baseprice,description=description,file1=file1_nm,file2=file2_nm,file3=file3_nm,file4=file4_nm,uid=uid,bstatus=bstatus,dt=dt)
        p.save()
        return render(request,"addproducts.html",{"clist":clist,"sunm":request.session['sunm'],"msg":"Product added successfully"})

def showSubcategory(request):
    catnm=request.GET.get("cnm")
    sclist=myadmin_model.Subcategory.objects.filter(catnm=catnm)
    sclist_options="<option>Select Sub Category</option>"
    for row in sclist:
        sclist_options+=("<option>"+row.subcatnm+"</option>")
    return HttpResponse(sclist_options)

def editprofileuser(request):
    userDetails=myapp_model.Register.objects.filter(username=request.session['sunm'])
    m,f=" "," "
    if userDetails[0].gender=="male":
        m="checked"
    else:
        f="checked"
    return render (request,"editprofileuser.html",{"sunm":request.session['sunm'],"userDetails":userDetails[0],"m":m,"f":f})

def updateDataUser(request):
    name=request.POST.get("name")
    email=request.POST.get("email")
    mobile=request.POST.get("mobile")
    address=request.POST.get("address")
    city=request.POST.get("city")
    gender=request.POST.get("gender")
    myapp_model.Register.objects.filter(username=email).update(name=name,mobile=mobile,address=address,city=city,gender=gender)
    return redirect("/user/editprofileuser")

def viewproductuser(request):
   paypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
   paypalID="sb-uzi2p4964129@business.example.com"
   pDetails=models.Products.objects.filter(uid=request.session['sunm'])
   return render(request,"viewproductuser.html",{"sunm":request.session['sunm'],"pDetails":pDetails,"media_url":media_url,"paypalURL":paypalURL,"paypalID":paypalID})

def payment(request):
    pid=request.GET.get('pid')
    price=request.GET.get('price')
    uid=request.GET.get('uid')
    dt=time.time()
    p=models.Payment(pid=int(pid),price=int(price),uid=uid,dt=dt)
    p.save
    models.Products.objects.filter(pid=int(pid)).update(bstatus=1,dt=dt)

    return redirect("/user/viewproductuser/")

def cancel(request):
    return render(request,"cancel.html",{'sunm':request.session['sunm']})

def viewbiddingproducts(request):
    scnm=request.GET.get("scnm")
    sunm=request.session["sunm"]
    pDetails=models.Products.objects.filter(~Q(uid=sunm),subcatnm=scnm) #"`" is a sign of negataion or not equal to or query formatter...negative negation is used so that the person who added product can't do bidding....it is a parameter    
    return render(request,"viewbiddingproducts.html",{'media_url':media_url,'sunm':request.session['sunm'],'pDetails':pDetails}) #for greater than (>) on orm we use "_lt"

def bidproduct(request):
    pid=request.GET.get("pid")
    pDetails=models.Products.objects.filter(pid=int(pid))
    stime=float(pDetails[0].dt)
    ctime=time.time()
    dtime=ctime-stime
    if dtime<192800:
        bDetails=models.Bidding.objects.filter(pid=int(pid))
        if len(bDetails)>0:
            max_cprice=bDetails[0].bprice        
            for row in bDetails:
                if max_cprice<row.bprice:
                    max_cprice=row.bprice
            cprice=max_cprice
        else:
            cprice=pDetails[0].baseprice                
        s=1    
    else:
        s=0
        cprice=None
    return render(request,"bidproduct.html",{'pDetails':pDetails,'sunm':request.session['sunm'],'s':s,'cprice':cprice})

def mybid(request):
    pid=request.POST.get('pid')
    bprice=request.POST.get('bprice')
    uid=request.session['sunm']
    dt=time.asctime()

    p=models.Bidding(pid=int(pid),bprice=int(bprice),uid=uid,dt=dt)
    p.save()
    
    return redirect('/user/bidproduct/?pid='+str(pid))

def viewbid(request):
    pid=request.GET.get('pid')
    bDetails=models.Bidding.objects.filter(pid=int(pid))
    return render(request,"viewbid.html",{'bDetails':bDetails,'sunm':request.session['sunm']})
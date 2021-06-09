
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.userhome),
    path('viewproducts/', views.viewproducts),
    path('subcatviewproducts/', views.subcatviewproducts),
    path('addproducts/', views.addproducts),
    path('showSubcategory/', views.showSubcategory),
    path('editprofileuser/',views.editprofileuser),
    path('updateDataUser/', views.updateDataUser),
    path('changepassworduser/', views.changepassworduser),
    path('viewproductuser/', views.viewproductuser),
    path('payment/',views.payment),
    path('cancel/',views.cancel),
    path('viewbiddingproducts/',views.viewbiddingproducts),
    path('bidproduct/',views.bidproduct),
    path('mybid/',views.mybid),
    path('viewbid/',views.viewbid)
]
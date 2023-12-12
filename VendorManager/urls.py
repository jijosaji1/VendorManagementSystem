from django.contrib import admin
from django.urls import path, include
from VendorManager import views

urlpatterns = [
    path('', views.vendor_details, name = "vendor_details"),
    path('<str:vendor_id>/', views.vendor, name = "vendor"),
    path('<str:vendor_id>/performance', views.vendor_performance, name = "vendor_performance"),
]
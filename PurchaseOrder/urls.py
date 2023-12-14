from django.contrib import admin
from django.urls import path, include
from PurchaseOrder import views

urlpatterns = [
    path('', views.order_details, name = "order_details"),
    path('<str:purchase_order_id>/', views.order, name = "order"),
    path('<str:purchase_order_id>/acknowledge', views.acknowledge, name = "order-acknowledge-ws"),
    path('<str:purchase_order_id>', views.order, name = "order-ws"),
    path('<str:purchase_order_id>/acknowledge/', views.acknowledge, name = "order-acknowledge")
]
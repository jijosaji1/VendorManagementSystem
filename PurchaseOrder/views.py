from datetime import datetime, timedelta, timezone
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from serializers import PurchaseOrderSerializer
from .models import PurchaseOrder
from VendorManager.models import Vendor
from VendorPerformance.views import save_changes_to_db

"""
Allows GET and POST request to /api/purchase_orders endpoint

Args:
    request: A http request.

Returns:
    Response: Response to the http request.
"""
@api_view(['GET', 'POST'])
def order_details(request):
    purchase_orders_vendor = None
    try:
        vendor_id = request.query_params.get("vendor", None)
        if vendor_id is not None:
            purchase_orders_vendor = PurchaseOrder.objects.filter(vendor=vendor_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            response = validate_post_data(serializer.validated_data)
            if response != None:
                return response
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        if purchase_orders_vendor is not None:
            serializer = PurchaseOrderSerializer(purchase_orders_vendor, many=True)
        else:
            purchase_orders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

"""
Allows GET, PUT and DELETE request to /api/purchase_orders/po_id endpoint

Args:
    request: A http request.

Returns:
    Response: Response to the http request.
"""
@api_view(['GET', 'PUT', 'DELETE'])
def order(request, purchase_order_id):
    try:
        purchase_orders = PurchaseOrder.objects.get(pk=purchase_order_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchase_orders, many=False)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchase_orders, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        purchase_orders.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Allows POST request to /api/purchase_orders/po_id/acknowledge endpoint

Args:
    request: A http request.

Returns:
    Response: Response to the http request.
"""
@api_view(['POST'])
def acknowledge(request, purchase_order_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
        purchase_order.acknowledgment_date = datetime.now(timezone.utc)
        purchase_order.save()
        vendor_id = purchase_order.vendor.vendor_id
        purchase_orders = PurchaseOrder.objects.filter(vendor=vendor_id)
        average_response_time = calculate_average_response_time(purchase_orders)
        Vendor.objects.filter(pk=purchase_order.vendor.vendor_id).update(average_response_time=average_response_time)
        save_changes_to_db(vendor_id, average_response_time=average_response_time)
        return Response(status=status.HTTP_201_CREATED)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

"""
Calculates average response time of each vendor on acknowledgment of a purchase order

Args:
    PurchaseOrder: purchase orders that has been acknowledged.

Returns:
    float: Average response time of the vendor.
"""
def calculate_average_response_time(purchase_orders):
    total_response_time = 0
    po_count = 0
    for purchase_order in purchase_orders:
        if purchase_order.acknowledgment_date is not None:
            response_time = (purchase_order.acknowledgment_date - purchase_order.issue_date)
            total_response_time += response_time.total_seconds()
            po_count += 1
    average_response_time = total_response_time / po_count
    return average_response_time

"""
Validates the purchase order details

Args:
    PurchaseOrder: purchase order that has been sent.

Returns:
    Response: Returns response if error occurs.
"""
def validate_post_data(purchase_order):
    try:
        total_item_quantity = 0
        order_date = purchase_order.get("order_date")
        delivery_date = purchase_order.get("delivery_date")
        issue_date = purchase_order.get("issue_date")
        quantity = purchase_order.get("quantity")
        items = purchase_order.get("items")
        if delivery_date <= order_date:
            return Response("Delivery date should not be less than order date", 
                            status=status.HTTP_400_BAD_REQUEST)
        if issue_date <= order_date or issue_date >= delivery_date:
            return Response("Issue date should be between order date and delivery date", 
                            status=status.HTTP_400_BAD_REQUEST)
        if quantity <= 0:
            return Response("Quantity can't be less than or equal to 0", status=status.HTTP_400_BAD_REQUEST)
        for item in items:
            total_item_quantity += items[item]
        if total_item_quantity != quantity:
            return Response("Total quantity and sum of quantities of individual items should be same",
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(f"Error with the data : {e}",
                            status=status.HTTP_400_BAD_REQUEST)

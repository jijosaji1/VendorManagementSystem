from datetime import datetime
from django.shortcuts import render
from .models import HistoricalPerformance
from VendorManager.models import Vendor

def save_changes_to_db(vendor_id, 
                       on_time_delivery_rate=0.0, 
                       quality_rating_avg=0.0, 
                       average_response_time=0.0,
                       fulfillment_rate=0.0):
    performance_model = HistoricalPerformance()
    performance_model.vendor = Vendor.objects.get(pk=vendor_id)
    performance_model.date = datetime.now()
    performance_model.on_time_delivery_rate = on_time_delivery_rate
    performance_model.quality_rating_avg = quality_rating_avg
    performance_model.average_response_time = average_response_time
    performance_model.fulfillment_rate = fulfillment_rate
    performance_model.save()

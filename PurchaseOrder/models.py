from datetime import datetime, timedelta, timezone
from django.db import models
from VendorManager.models import Vendor
from django.db.models.signals import pre_save
from django.dispatch import receiver
from VendorPerformance.views import save_changes_to_db

class PurchaseOrder(models.Model):
    po_id = models.AutoField(primary_key=True)
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

"""
Function to perform actions before saving any entry to the PurchaseOrder model
"""
@receiver(pre_save, sender = PurchaseOrder)
def purchase_order_change(sender, instance, **kwargs):
    on_time_delivery_rate = 0.0
    avg_quality_rating = 0.0
    fulfillment_rate = 0.0
    try:
        purchase_order = sender.objects.get(po_id=instance.po_id)
        vendor_id = instance.vendor.vendor_id
        if purchase_order.status != instance.status and instance.status == "completed":
            if ((purchase_order.delivery_date - datetime.now(timezone.utc)).total_seconds()) > 0:
                before_time = 1
            else:
                before_time = 0
            vendor = Vendor.objects.get(pk=vendor_id)
            completed_order_count = sender.objects.filter(vendor=vendor_id, status="completed").count()
            on_time_delivery_rate = (vendor.on_time_delivery_rate * completed_order_count + before_time)/(completed_order_count + 1)
            Vendor.objects.filter(pk=vendor_id).update(on_time_delivery_rate=on_time_delivery_rate)
        if purchase_order.quality_rating != instance.quality_rating and instance.quality_rating is not None:
            total_quality_rating = 0
            total_no_of_rated_orders = 0
            vendor_purchase_orders = sender.objects.filter(vendor=vendor_id)
            for purchase_order in vendor_purchase_orders:
                if purchase_order.quality_rating != None:
                    total_quality_rating += purchase_order.quality_rating
                    total_no_of_rated_orders += 1
            avg_quality_rating = (total_quality_rating + instance.quality_rating)/(total_no_of_rated_orders + 1)
            Vendor.objects.filter(pk=vendor_id).update(quality_rating_avg=avg_quality_rating)
        if purchase_order.status != instance.status:
            count = 0
            if instance.status == "completed":
                count = 1
            fulfilled_order_count = sender.objects.filter(vendor=vendor_id, status="completed").count()
            total_issued_order_count = sender.objects.filter(vendor=vendor_id).count()
            fulfillment_rate = (fulfilled_order_count + count)/total_issued_order_count
            Vendor.objects.filter(pk=vendor_id).update(fulfillment_rate=fulfillment_rate)
        if on_time_delivery_rate==0.0 and avg_quality_rating==0.0 and fulfillment_rate==0.0:
            return
        save_changes_to_db(vendor_id=vendor_id,
                            on_time_delivery_rate=on_time_delivery_rate,
                            quality_rating_avg=avg_quality_rating,
                            fulfillment_rate=fulfillment_rate)
    except PurchaseOrder.DoesNotExist:
        pass

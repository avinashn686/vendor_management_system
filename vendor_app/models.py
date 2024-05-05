from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0) 
    quality_rating_avg = models.FloatField(default=0) 
    average_response_time = models.FloatField(default=0) 
    fulfillment_rate = models.FloatField(default=0) 

    def __str__(self):
        return self.name
    

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=0) 
    delivery_date = models.DateTimeField(default=0) 
    items = models.JSONField()
    quantity = models.IntegerField(default=0) 
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number
    def save(self, *args, **kwargs):
        if self.pk:
            # Fetch the original object from the database
            original = PurchaseOrder.objects.get(pk=self.pk)
            # Store the original status in _origin_status attribute
            self._origin_status = original.status
        super(PurchaseOrder, self).save(*args, **kwargs)
    
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField(default=0) 
    quality_rating_avg = models.FloatField(default=0) 
    average_response_time = models.FloatField(default=0) 
    fulfillment_rate = models.FloatField(default=0) 

    def __str__(self):
        return f"{self.vendor} - {self.date}"

@receiver(post_save, sender=PurchaseOrder)   
def update_historical_performance(sender, instance, created, **kwargs):
    # Check if a new purchase order is created or an existing one is updated
    if created or instance.pk is None or instance.status != instance._origin_status:
        # Calculate vendor performance metrics
        # Update or create HistoricalPerformance records accordingly
        # Save the changes to the HistoricalPerformance table
        # Example:
        vendor = instance.vendor
        historical_performance = HistoricalPerformance.objects.create(
            vendor=vendor,
            date=timezone.now(),
            on_time_delivery_rate=vendor.on_time_delivery_rate,
            quality_rating_avg=vendor.quality_rating_avg,
            average_response_time=vendor.average_response_time,
            fulfillment_rate=vendor.fulfillment_rate,
        )
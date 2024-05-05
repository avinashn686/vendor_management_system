from django.shortcuts import render
from django.db.models import Avg, Count
from django.db.models import Avg, Count, F, Q
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
# Create your views here.
from rest_framework import viewsets
from .models import HistoricalPerformance, PurchaseOrder, Vendor
from .serializers import HistoricalPerformanceSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer, VendorSerializer

def update_vendor_performance_metrics(vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)

        # Calculate On-Time Delivery Rate
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_delivery_count = completed_orders.filter(delivery_date__lte=F('acknowledgment_date')).count()
        total_completed_orders = completed_orders.count()
        vendor.on_time_delivery_rate = (on_time_delivery_count / total_completed_orders) * 100 if total_completed_orders else 0

        # Calculate Quality Rating Average
        vendor.quality_rating_avg = completed_orders.filter(quality_rating__isnull=False).aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

        # Calculate Average Response Time
        response_times = completed_orders.exclude(acknowledgment_date=None).annotate(response_time=F('acknowledgment_date') - F('issue_date')).aggregate(Avg('response_time'))['response_time__avg']
        vendor.average_response_time = response_times.total_seconds() / 60 if response_times else 0

        # Calculate Fulfilment Rate
        fulfilled_orders = completed_orders.filter(Q(issue_date__lte=F('acknowledgment_date')) | Q(issue_date__isnull=True))
        vendor.fulfillment_rate = (fulfilled_orders.count() / total_completed_orders) * 100 if total_completed_orders else 0

        vendor.save()
    except Vendor.DoesNotExist:
        pass

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer



class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        vendor = Vendor.objects.get(pk=vendor_id)
        serializer = VendorPerformanceSerializer(vendor)
        return Response(serializer.data)

class AcknowledgePurchaseOrderView(APIView):
    def post(self, request, pk):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()
            
            # Update vendor performance metrics
            update_vendor_performance_metrics(purchase_order.vendor_id)
            
            return Response({"message": "Done"}, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class HistoricalPerformanceView(APIView):
    def get(self, request, vendor_id):
        try:
            history_data = HistoricalPerformance.objects.filter(vendor=vendor_id)
            serializer = HistoricalPerformanceSerializer(history_data, many=True)
            return Response(serializer.data)
        except HistoricalPerformance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
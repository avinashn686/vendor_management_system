from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AcknowledgePurchaseOrderView, HistoricalPerformanceView, PurchaseOrderViewSet, VendorPerformanceView, VendorViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),
    path('vendors/<int:vendor_id>/historical_performance/', HistoricalPerformanceView.as_view(), name='historical-performance'),
]
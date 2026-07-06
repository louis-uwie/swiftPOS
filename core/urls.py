from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, ProductViewSet, PurchaseOrderViewSet, SaleViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'products', ProductViewSet)
router.register(r'purchase-orders', PurchaseOrderViewSet)
router.register(r'sales', SaleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
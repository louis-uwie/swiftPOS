from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import User, Supplier, Product, PurchaseOrder, PurchaseOrderItem, Sale, SaleItem
from .serializers import (
    UserSerializer, SupplierSerializer, ProductSerializer,
    PurchaseOrderSerializer, SaleSerializer
)

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'admin'

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdmin]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low = Product.objects.filter(stock__lte=models.F('low_stock_threshold'))
        return Response(ProductSerializer(low, many=True).data)

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAdmin]

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        from django.utils import timezone
        today = timezone.now().date()
        sales = Sale.objects.filter(created_at__date=today)
        total = sales.aggregate(total=Sum('total'))['total'] or 0
        return Response({
            'date': today,
            'total_sales': sales.count(),
            'total_revenue': total
        })
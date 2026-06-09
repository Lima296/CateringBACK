from rest_framework import viewsets, response, decorators
from .models import Venta
from .serializers import VentaSerializer
from django.db.models import Sum, F

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by('-fecha')
    serializer_class = VentaSerializer

    @decorators.action(detail=False, methods=['get'])
    def resumen_financiero(self, request):
        total_ingresos = Venta.objects.aggregate(total=Sum('precio_total'))['total'] or 0
        total_costos = Venta.objects.aggregate(total=Sum('costo_total'))['total'] or 0
        ganancia_neta = total_ingresos - total_costos
        
        # Margen promedio
        margen_porcentual = (ganancia_neta / total_ingresos * 100) if total_ingresos > 0 else 0

        return response.Response({
            'total_ingresos': total_ingresos,
            'total_costos': total_costos,
            'ganancia_neta': ganancia_neta,
            'margen_porcentual': round(margen_porcentual, 2),
            'cantidad_ventas': Venta.objects.count()
        })

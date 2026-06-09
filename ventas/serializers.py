from rest_framework import serializers
from .models import Venta
from recetas.models import Receta

class VentaSerializer(serializers.ModelSerializer):
    receta_nombre = serializers.ReadOnlyField(source='receta.nombre')
    margen = serializers.ReadOnlyField(source='margen_ganancia')

    class Meta:
        model = Venta
        fields = ['id', 'receta', 'receta_nombre', 'cantidad', 'precio_total', 'costo_total', 'fecha', 'cliente', 'margen']
        read_only_fields = ['costo_total', 'fecha']

    def create(self, validated_data):
        receta = validated_data['receta']
        cantidad = validated_data['cantidad']
        
        # Calcular el costo actual de la receta
        detalles = receta.detalles.all()
        costo_unitario = sum(item.cantidad_usada * item.ingrediente.costo for item in detalles)
        
        validated_data['costo_total'] = costo_unitario * cantidad
        return super().create(validated_data)

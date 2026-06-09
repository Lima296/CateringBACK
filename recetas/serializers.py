from rest_framework import serializers
from .models import Receta, IngredienteReceta
from ingredientes.serializers import IngredienteSerializer

class IngredienteRecetaSerializer(serializers.ModelSerializer):
    costo_subtotal = serializers.SerializerMethodField()
    ingrediente_nombre = serializers.ReadOnlyField(source='ingrediente.nombre')

    class Meta:
        model = IngredienteReceta
        fields = ['id', 'ingrediente', 'ingrediente_nombre', 'cantidad_usada', 'costo_subtotal']

    def get_costo_subtotal(self, obj):
        return obj.cantidad_usada * obj.ingrediente.costo

class RecetaSerializer(serializers.ModelSerializer):
    detalles = IngredienteRecetaSerializer(many=True, read_only=True)
    ingredientes_input = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    costo_total = serializers.SerializerMethodField()

    class Meta:
        model = Receta
        fields = ['id', 'nombre', 'descripcion', 'detalles', 'ingredientes_input', 'costo_total']

    def get_costo_total(self, obj):
        detalles = obj.detalles.all()
        return sum(item.cantidad_usada * item.ingrediente.costo for item in detalles)

    def create(self, validated_data):
        ingredientes_data = validated_data.pop('ingredientes_input', [])
        receta = Receta.objects.create(**validated_data)
        for item in ingredientes_data:
            IngredienteReceta.objects.create(
                receta=receta,
                ingrediente_id=item['ingrediente'],
                cantidad_usada=item['cantidad_usada']
            )
        return receta

    def update(self, instance, validated_data):
        ingredientes_data = validated_data.pop('ingredientes_input', None)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.save()

        if ingredientes_data is not None:
            # Opción simple: borrar y recrear detalles
            instance.detalles.all().delete()
            for item in ingredientes_data:
                IngredienteReceta.objects.create(
                    receta=instance,
                    ingrediente_id=item['ingrediente'],
                    cantidad_usada=item['cantidad_usada']
                )
        return instance

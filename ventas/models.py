import uuid
from django.db import models
from recetas.models import Receta

class Venta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='ventas')
    cantidad = models.PositiveIntegerField(default=1)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2)
    costo_total = models.DecimalField(max_digits=12, decimal_places=2, help_text="Costo de la receta al momento de la venta")
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Venta {self.id} - {self.receta.nombre}"

    @property
    def margen_ganancia(self):
        return self.precio_total - self.costo_total

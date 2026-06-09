import uuid
from django.db import models

class Ingrediente(models.Model):
    CATEGORIAS = [
        ('VERDULERIA', 'Verdulería'),
        ('CARNES', 'Carnes'),
        ('ALMACEN', 'Almacén'),
    ]
    UNIDADES = [
        ('KG', 'Kilogramo'),
        ('L', 'Litro'),
        ('UN', 'Unidad'),
        ('GR', 'Gramo'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    unidad_medida = models.CharField(max_length=10, choices=UNIDADES, default='UN')
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} ({self.unidad_medida})"

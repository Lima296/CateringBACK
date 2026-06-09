import uuid
from django.db import models
from ingredientes.models import Ingrediente

class Receta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    ingredientes = models.ManyToManyField(Ingrediente, through='IngredienteReceta')

    def __str__(self):
        return self.nombre

class IngredienteReceta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='detalles')
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad_usada = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"{self.cantidad_usada} de {self.ingrediente.nombre} en {self.receta.nombre}"

from django.db import models

# Create your models here.

class Cliente(models.Model):
    nombre_cliente = models.CharField(max_length=300)
    clave = models.CharField(max_length=300, default="")
    celular = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.nombre_cliente} - {self.clave} - {self.celular}"

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(null=True, auto_now_add=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    fecha_entregado = models.DateTimeField(null=True, blank=True)
    descripcion = models.CharField(max_length=300, null=True, blank=True)
    tamano = models.CharField(max_length=300, null=True, blank=True)
    costo = models.CharField(max_length=300, null=True, blank=True)
    anticipo = models.CharField(max_length=300, null=True, blank=True)
    restante = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estatus = models.IntegerField(default=1) 
    imagen = models.BinaryField(null=True, blank=True)
    imagenUrl = models.ImageField(upload_to='images/' , null=True)
    celular = models.CharField(max_length=100,blank=True)
    imagenUrlExternal = models.TextField(default="")

    def __str__(self):
        return f"Cliente: {self.cliente} - Fecha de Creación: {self.fecha_creacion} - Fecha de Entrega: {self.fecha_entrega} - Descripción: {self.descripcion} - Tamaño: {self.tamano} - Costo: {self.costo} - Anticipo: {self.anticipo} - Restante: {self.restante} - Estatus: {self.estatus}"
from django.db import models

# Create your models here.

class Cliente(models.Model):
    nombre_cliente = models.CharField(max_length=300)
    clave = models.CharField(max_length=300, default="")
    celular = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.nombre_cliente} - {self.clave} - {self.celular}"

class Pedido(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]
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
    #imagenUrl = models.ImageField(upload_to='images/' , null=True)
    celular = models.CharField(max_length=100,blank=True)
    imagenUrlExternal = models.TextField(default="")

    def __str__(self):
        return f"Cliente: {self.cliente} - Fecha de Creación: {self.fecha_creacion} - Fecha de Entrega: {self.fecha_entrega} - Descripción: {self.descripcion} - Tamaño: {self.tamano} - Costo: {self.costo} - Anticipo: {self.anticipo} - Restante: {self.restante} - Estatus: {self.estatus}"

class Cuenta(models.Model):
    """
    Un renglon por mes (unico por anio+mes) con el ingreso/gasto/total del
    mes, calculados a partir de sus MovimientoCuenta (ver
    recalcular_totales). Al entrar a la pantalla de Cuentas, se busca (o se crea en 0) el
    renglon del mes/anio actual -- si cambio el mes desde la ultima vez
    que se abrio, se crea uno nuevo en 0 y el anterior queda fijo como
    parte del historial (ver HistorialCuentasAPIView, que es simplemente
    el listado de estos renglones).
    """
    class Meta:
        unique_together = ('anio', 'mes')
        indexes = [
            models.Index(fields=['anio', 'mes']),
        ]
        ordering = ['-anio', '-mes']

    anio = models.IntegerField()
    mes = models.IntegerField()  # 1-12
    ingreso = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    gasto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_creacion = models.DateTimeField(null=True, auto_now_add=True, blank=True)
    fecha_actualizacion = models.DateTimeField(null=True, auto_now=True, blank=True)

    def __str__(self):
        return f"{self.mes}/{self.anio} - Ingreso: {self.ingreso} - Gasto: {self.gasto} - Total: {self.total}"

    def recalcular_totales(self):
        """
        Ingreso/gasto/total del mes ya no se capturan a mano: son la suma
        de sus MovimientoCuenta. Hay que llamarlo cada vez que se crea,
        edita o borra un movimiento del mes.
        """
        sumas = self.movimientos.values('tipo').annotate(suma=models.Sum('monto'))
        por_tipo = {fila['tipo']: fila['suma'] or 0 for fila in sumas}
        self.ingreso = por_tipo.get(MovimientoCuenta.TIPO_INGRESO, 0)
        self.gasto = por_tipo.get(MovimientoCuenta.TIPO_GASTO, 0)
        self.total = self.ingreso - self.gasto
        self.save()


class MovimientoCuenta(models.Model):
    """
    Desglose de la Cuenta del mes: un renglon por cada ingreso o gasto,
    con su fecha y descripcion (para saber en que se fue el dinero).
    """
    TIPO_INGRESO = 'ingreso'
    TIPO_GASTO = 'gasto'
    TIPOS = [
        (TIPO_INGRESO, 'Ingreso'),
        (TIPO_GASTO, 'Gasto'),
    ]

    class Meta:
        ordering = ['fecha', 'id']

    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='movimientos')
    fecha = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPOS)
    descripcion = models.CharField(max_length=300, blank=True, default='')
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_creacion = models.DateTimeField(null=True, auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.fecha} - {self.tipo} - {self.descripcion} - {self.monto}"
from rest_framework import serializers
from .models import Cliente, Pedido, Cuenta


class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'nombre_cliente', 'clave', 'celular',)

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        cliente = ClientesSerializer(many=True, read_only=False)
        fields = ('id', 'cliente', 'fecha_creacion', 'fecha_entrega', 'descripcion', 'tamano', 'costo', 'anticipo', 'restante', 'estatus','celular','imagenUrlExternal',)
        depth = 1

class HistoricoPedidoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source="cliente.nombre_cliente", read_only=True)
    estatus_display = serializers.SerializerMethodField()
    fecha_entrega_formateada = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = [
            'id',
            'fecha_entrega',
            'fecha_entrega_formateada',
            'estatus',
            'estatus_display',
            'descripcion',
            'cliente_nombre'
        ]

    def get_estatus_display(self, obj):
        mapping = {
            0: "Cancelado",
            1: "En espera",
            2: "Entregado"
        }
        return mapping.get(obj.estatus, "Desconocido")
    
    def get_fecha_entrega_formateada(self, obj):
        if obj.fecha_entrega:
            return obj.fecha_entrega.strftime("%H:%M %d/%m/%Y")
        return ""

class CuentaSerializer(serializers.ModelSerializer):
    fecha_formateada = serializers.SerializerMethodField()

    class Meta:
        model = Cuenta
        fields = ('id', 'fecha', 'fecha_formateada', 'ingreso', 'gasto', 'total')

    def get_fecha_formateada(self, obj):
        if obj.fecha:
            return obj.fecha.strftime("%d/%m/%Y")
        return ""
    
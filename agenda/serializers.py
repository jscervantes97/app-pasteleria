from rest_framework import serializers 
from .models import Cliente, Pedido


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

    class Meta:
        model = Pedido
        fields = [
            'id',
            'fecha_entrega',
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
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
        fields = ('id', 'cliente', 'fecha_creacion', 'fecha_entrega', 'descripcion', 'tamano', 'costo', 'anticipo', 'restante', 'estatus',)
        depth = 1

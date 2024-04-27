from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pedido
from .serializers import PedidoSerializer
from .filters import PedidoFilter


class PedidosViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer

    def get_queryset(self):
        pedidos = Pedido.objects.all()
        return pedidos
    
class PedidoList(generics.ListAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    filterset_class = PedidoFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset_filtered = self.filterset_class(self.request.query_params, queryset=queryset).qs
        #print(queryset_filtered.query)  # Imprimir la consulta SQL generada
        return queryset_filtered
    
class ActualizarEstadoPedido(APIView):
    def patch(self, request, format=None):
        try:
            pedido_id = request.data.get('idPedido')
            nuevo_estado = request.data.get('estado')

            pedido = Pedido.objects.get(pk=pedido_id)
        except Pedido.DoesNotExist:
            return Response({"error": "El pedido no existe."}, status=status.HTTP_404_NOT_FOUND)

        pedido.estatus = nuevo_estado
        pedido.save()
        return Response({"msg": "Exito"})
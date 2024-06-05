
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import Pedido, Cliente
from .serializers import PedidoSerializer
from .filters import PedidoFilter
from decimal import Decimal





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
    
class PedidoDetalle(generics.RetrieveAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    lookup_field = 'id' 


@api_view(['POST', 'PATCH'])
def crearactualizarpedido(request):
    cveCliente = request.data.get('nombreCliente')
    
    if Cliente.objects.filter(nombre_cliente=cveCliente).exists(): 
        cliente = Cliente.objects.get(nombre_cliente=cveCliente)
        if request.data.get('celular') not in cliente.celular :
            cliente.celular = cliente.celular + ',' + request.data.get('celular')
        cliente.save()
    else:
        cliente = Cliente(nombre_cliente = request.data.get('nombreCliente'), clave = cveCliente.strip().upper(), celular = request.data.get('celular'))
        cliente.save()

    if request.method == 'POST':
        pedido = Pedido(cliente=cliente, fecha_entrega=request.data.get('fechaEntrega'),
                        descripcion=request.data.get('descripcion'), tamano=request.data.get('tamano'),
                        costo=request.data.get('costo'), anticipo=request.data.get('anticipo'), restante = 0.0 )
        pedido.save()
        return Response({"message": "Exito al crar el nuevo pedido", "idPedido" : pedido.id}, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        idPedido = request.data.get('idPedido')
        pedido = get_object_or_404(Pedido , pk = idPedido)
        pedido.fecha_entrega = request.data.get('fechaEntrega')
        pedido.descripcion = request.data.get('descripcion')
        pedido.tamano = request.data.get('tamano')
        pedido.costo = request.data.get('costo')
        pedido.anticipo = request.data.get('anticipo')
        pedido.restante = 0.0
        pedido.cliente = cliente
        pedido.save()
        return Response({"message": "Exito al actualizar los datos de pedido"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "No Supported method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST', 'PATCH'])
def crearactualizarimagenpedido(request):
    # Obtener los datos de la solicitud
    pedido_id = request.POST.get('idPedido')
    imagen = request.FILES.get('imagen')
    
    print(pedido_id)
    print(imagen)
    # Verificar si el pedido existe
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Actualizar o crear la imagen asociada al pedido
    if imagen:
        pedido.imagen = imagen.read()
        pedido.save()
        return Response({'detail': 'Imagen actualizada correctamente'}, status=status.HTTP_200_OK)
    else:
        #pedido.imagen = None
        #pedido.save()
        return Response({'detail': 'Se guardo el registro sin imagen'}, status=status.HTTP_200_OK)

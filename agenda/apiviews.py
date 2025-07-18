import requests
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import Pedido, Cliente
from .serializers import PedidoSerializer, HistoricoPedidoSerializer
from .filters import PedidoFilter

from django.db.models import Q


import requests
from dotenv import load_dotenv
import os

# Cargar las variables desde el archivo .env
load_dotenv()

# Acceder a las variables de entorno






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
            print('ya existe')
        
    else:
        cliente = Cliente(nombre_cliente = request.data.get('nombreCliente'), clave = cveCliente.strip().upper(), celular = request.data.get('celular'))
        cliente.save()

    if request.method == 'POST':
        pedido = Pedido(cliente=cliente, fecha_entrega=request.data.get('fechaEntrega'),
                        descripcion=request.data.get('descripcion'), tamano=request.data.get('tamano'),
                        costo=request.data.get('costo'), anticipo=request.data.get('anticipo'), restante = 0.0, celular = request.data.get('celular'))
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
        pedido.celular = request.data.get('celular')
        pedido.save()  
        return Response({"message": "Exito al actualizar los datos de pedido"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "No Supported method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST', 'PATCH'])
def crearactualizarimagenpedido(request):
    print("Empieza metodo de crear actualizar imagen pedido")
    # Obtener los datos de la solicitud
    pedido_id = request.POST.get('idPedido')
    imagen = request.FILES.get('imagen')
    
    print("id pedido")
    print(pedido_id)
    print("Datos de la imagen")
    print(imagen)
    
    # Verificar si el pedido existe
    pedido = get_object_or_404(Pedido, id=pedido_id)
    token = os.getenv('API_FILES_TOKEN')  # Busca la variable en el .env o en el entorno del sistema
    if not token:
        return Response(
            {'detail': 'El token de autenticación no está configurado.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if not pedido_id:
        return Response(
            {'detail': 'El id pedido no fue proporcionado'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


    # Actualizar o crear la imagen asociada al pedido
    if imagen:
        print("El pedido a guardar/crear viene con una imagen")
        url_server = os.getenv('URL_FILES_SERVER')
        # Subir la imagen a otra URL mediante POST
        url_destino = f"{url_server}/sieslite-files-api/upload"  # Cambia esto por la URL de tu API
        headers = {
            "Authorization": f"Token {token}",  # Autenticación con token
        }
        archivos = {'image': (imagen.name, imagen, imagen.content_type)}  # Cambiar a 'image' según el endpoint
        data = {'idPedido': pedido_id}  # Agregar el ID del pedido

        try:
            # Realizar la petición POST para subir la imagen
            response = requests.post(url_destino, files=archivos, data=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("Se guardo la imagen en el servidor del proxy")
                # Procesar la respuesta exitosa
                respuesta_json = response.json()
                image_url = respuesta_json.get("url")  # URL de la imagen proporcionada por la API externa

                # Actualizar los datos en el modelo local
                #pedido.imagen = None
                #pedido.imagenUrl = imagen  # Guardar la URL devuelta por la API
                #pedido.imagenUrlExternal = image_urlg
                pedido.imagenUrlExternal = f"{url_server}/{image_url}"
                pedido.save()
                print(f"Se guardo la imagen del pedido con la url externa {url_server}/{image_url}")
                return Response(
                    {'detail': 'Imagen actualizada y subida correctamente', 'url': image_url},
                    status=status.HTTP_200_OK
                )
            else:
                # Error en la API externa
                print(f"Errpr al subir la imagen con el id pedido {pedido_id}")
                return Response(
                    {'detail': f'Error al subir la imagen: {response.content.decode("utf-8")}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except requests.exceptions.RequestException as e:
            # Error de conexión u otro problema con la API externa
            print("Ocurrio otro tipo de error")
            return Response(
                {'detail': f'Error al conectarse al servidor de imágenes: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        # Guardar el pedido sin imagen
        print(f"el pedido {pedido_id} se guardo sin ninguna imagen")
        #pedido.imagen = None
        pedido.save()
        return Response({'detail': 'Se guardó el registro sin imagen'}, status=status.HTTP_200_OK)

class PedidoDatatableAPIView(APIView):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "")

        pedidos = Pedido.objects.select_related('cliente').order_by('id')

        if search_value:
            pedidos = pedidos.filter(
                Q(descripcion__icontains=search_value) |
                Q(cliente__nombre_cliente__icontains=search_value)
            )

        total = pedidos.count()
        pedidos = pedidos[start:start + length]

        serializer = HistoricoPedidoSerializer(pedidos, many=True)

        return Response({
            "draw": draw,
            "recordsTotal": total,
            "recordsFiltered": total,
            "data": serializer.data
        })


"""
@api_view(['POST'])
def crearactualizarimagenpedidoMazivo(request):
    # Obtener los datos de la solicitud
    pedido_id = request.POST.get('idPedido')
    imagen = request.FILES.get('imagen')
    
    print(pedido_id)
    print(imagen)
    
    # Verificar si el pedido existe
    token = os.getenv('API_FILES_TOKEN')  # Busca la variable en el .env o en el entorno del sistema
    if not token:
        return Response(
            {'detail': 'El token de autenticación no está configurado.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Actualizar o crear la imagen asociada al pedido
    if imagen:
        # Subir la imagen a otra URL mediante POST
        url_server = os.getenv('URL_FILES_SERVER')
        url_destino = f"{url_server}/sieslite-files-api/upload"  # Cambia esto por la URL de tu API
        headers = {
            "Authorization": f"Token {token}",  # Autenticación con token
        }
        archivos = {'image': (imagen.name, imagen, imagen.content_type)}  # Cambiar a 'image' según el endpoint
        data = {'idPedido': pedido_id}  # Agregar el ID del pedido

        try:
            # Realizar la petición POST para subir la imagen
            response = requests.post(url_destino, files=archivos, data=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Procesar la respuesta exitosa
                respuesta_json = response.json()
                image_url = respuesta_json.get("url")  # URL de la imagen proporcionada por la API externa

                # Actualizar los datos en el modelo local

                return Response(
                    {'detail': 'Imagen actualizada y subida correctamente', 'url': image_url},
                    status=status.HTTP_200_OK
                )
            else:
                # Error en la API externa
                return Response(
                    {'detail': f'Error al subir la imagen con id {pedido_id} response: {response.content.decode("utf-8")}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except requests.exceptions.RequestException as e:
            # Error de conexión u otro problema con la API externa
            return Response(
                {'detail': f'Error al conectarse al servidor de imágenes: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        # Guardar el pedido sin imagen
        return Response({'detail': 'Se guardó el registro sin imagen'}, status=status.HTTP_200_OK)
"""   

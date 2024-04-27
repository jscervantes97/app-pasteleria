from django.urls import path
from rest_framework import routers
from .apiviews import PedidosViewSet, PedidoList, ActualizarEstadoPedido



router = routers.DefaultRouter()

#router.register('api/pedidos' , PedidosViewSet, 'pedidos')

router.register(r'api/pedidos', PedidosViewSet, basename='pedidos')



urlpatterns = [
    path('api/pedidos/', PedidoList.as_view(), name='pedido-list'),
    path('api/pedidos/actualizarestado', ActualizarEstadoPedido.as_view(), name='actualizar_estado_pedido'),
]

urlpatterns += router.urls
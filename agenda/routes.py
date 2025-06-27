from django.urls import path
from rest_framework import routers
from .apiviews import PedidosViewSet, PedidoList, ActualizarEstadoPedido, crearactualizarpedido,PedidoDetalle, crearactualizarimagenpedido, PedidoDatatableAPIView



router = routers.DefaultRouter()

#router.register('api/pedidos' , PedidosViewSet, 'pedidos')

router.register(r'api/pedidos', PedidosViewSet, basename='pedidos')



urlpatterns = [
    path('api/pedidos/', PedidoList.as_view(), name='pedido-list'),
    path('api/pedidos/actualizarestado', ActualizarEstadoPedido.as_view(), name='actualizar_estado_pedido'),
    path('api/pedidos/crearactualizar', crearactualizarpedido, name='crearactualizar'),
    path('api/pedidos/imagen', crearactualizarimagenpedido, name='crearactualizarimagenpedido'),
    path('api/pedidos/<int:id>/', PedidoDetalle.as_view(), name='pedido-detalle'),
    path('api/pedidos/datatable/', PedidoDatatableAPIView.as_view(), name='api_pedidos_datatable'),

]

urlpatterns += router.urls
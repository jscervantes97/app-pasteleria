from django.urls import path 
from .views import goindex, renderlogin, renderpedido, saveupdatepedido, renderhistorial, renderexample, renderSubidorImagenes

urlpatterns = [
    path('' , goindex),
    path('login', renderlogin),
    path('historial', renderhistorial),
    path('pedido', renderpedido),
    path('pedido/', renderpedido),
    path('pedido/<int:idPedido>', renderpedido),
    path('pedido/nuevo', saveupdatepedido, name="create_pedido"),
    path('example', renderexample),
    path('subidorimagenes', renderSubidorImagenes),

]
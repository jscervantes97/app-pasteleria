from django.urls import path
from .views import goindex, renderlogin, renderpedido, saveupdatepedido, renderhistorial, renderexample, renderSubidorImagenes, rendercuentas, rendercuenta

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
    path('cuentas', rendercuentas),
    path('cuenta', rendercuenta),
    path('cuenta/', rendercuenta),
    path('cuenta/<int:idCuenta>', rendercuenta),

]
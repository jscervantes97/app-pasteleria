from .models import Pedido
import datetime
def message_processor(request):
    hoy = datetime.datetime.now().strftime ("%Y-%m-%d")
    print('pedidos pa hoy' + hoy)
    pedidosHoy = Pedido.objects.filter(fecha_entrega__startswith=hoy).count()
    return {
        'pedidosHoy' : pedidosHoy
    }
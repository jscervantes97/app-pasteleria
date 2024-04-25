from django.shortcuts import render
from .models import Cliente, Pedido

# Create your views here.
def goindex(request):
    #pedidos = Pedido.objects.all().order_by('fecha_entrega').values()
    pedidos = Pedido.objects.all().order_by('fecha_entrega')
    
    return render(request, 'index.html', { "pedidos" : pedidos })

def renderlogin(request):
    return render(request, 'login.html')

def renderhistorial(request):
    clientes = Cliente.objects.all()
    pedidos = Pedido.objects.all()
    return render(request, 'historial.html', {
        "clientes" : clientes,
        "pedidos" : pedidos
    })

def renderpedido(request, idPedido=None):
    tituloForm = 'Editar Pedido'
    listaClientes = Cliente.objects.all()
    if idPedido is None:
        tituloForm = 'Nuevo Pedido'
        pedido = Pedido()
    else:
        pedido = Pedido.objects.get(pk=idPedido)

    #print(pedido)   
    return render(request, 'pedido.html', { 
        "idPedido" : idPedido, 
        "tituloForm" : tituloForm, 
        "descripcion" : "dato example",
        "clientes" : listaClientes })

def saveupdatepedido(request, idPedido=None):
    if idPedido is None:
       cveCliente = request.POST['nombreCliente']
       print(cveCliente.strip().upper())
       if Cliente.objects.filter(nombre_cliente=cveCliente).exists(): 
           cliente = Cliente.objects.get(nombre_cliente=cveCliente)
       else:
            cliente = Cliente(nombre_cliente = request.POST['nombreCliente'], clave = cveCliente.strip().upper(), celular = request.POST['celular'])
            cliente.save()

       pedido = Pedido(cliente=cliente, fecha_entrega=request.POST['fechaEntrega'],
                       descripcion=request.POST['descripcion'], tamano=request.POST['tamano'],
                       costo=request.POST['costo'], anticipo=request.POST['anticipo'], restante = (int(request.POST['costo']) - int(request.POST['anticipo'])))
       pedido.save()


    return render(request , 'index.html')

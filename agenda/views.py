from django.shortcuts import render, redirect
from .models import Cliente, Pedido



# Create your views here.
def goindex(request):
    #pedidos = Pedido.objects.all().order_by('fecha_entrega').values()
    pedidos = Pedido.objects.filter(estatus=1).order_by('fecha_entrega')
    
    return render(request, 'index.html', { "pedidos" : pedidos })

def renderexample(request):
    
    return render(request, 'htmlexample.html', )

def renderlogin(request):
    return render(request, 'login.html')

def renderhistorial(request):
    #clientes = Cliente.objects.all()
    print("Ejecutando renderhistorial")
    #pedidos = Pedido.objects.all()[:10]
    #print(pedidos)
    return render(request, 'historial.html', {
        "pedidos" : None
    })



def renderpedido(request, idPedido=None):
    tituloForm = 'Editar Pedido'
    listaClientes = Cliente.objects.all()
    if idPedido is None:
        tituloForm = 'Nuevo Pedido'
        pedido = Pedido()
    else:
        pedido = Pedido.objects.get(pk=idPedido)

    
    #objeto = vars(pedido)
    #print(objeto) 
    return render(request, 'pedido.html', { 
        "idPedido" : idPedido, 
        "tituloForm" : tituloForm, 
        "descripcion" : "dato example",
        "pedido": pedido,
        "clientes" : listaClientes })

def saveupdatepedido(request, idPedido=None):
    if idPedido is None:
        cveCliente = request.POST['nombreCliente']
        print(cveCliente.strip().upper())
        if Cliente.objects.filter(nombre_cliente=cveCliente).exists(): 
            cliente = Cliente.objects.get(nombre_cliente=cveCliente)
            if cliente.celular != request.POST['celular']:
                cliente.celular = cliente.celular + ',' + request.POST['celular']
            cliente.save()
        else:
            cliente = Cliente(nombre_cliente=request.POST['nombreCliente'], clave=cveCliente.strip().upper(), celular=request.POST['celular'])
            cliente.save()

        pedido = Pedido(cliente=cliente, fecha_entrega=request.POST['fechaEntrega'],
                        descripcion=request.POST['descripcion'], tamano=request.POST['tamano'],
                        costo=request.POST['costo'], anticipo=request.POST['anticipo'], restante=(int(request.POST['costo']) - int(request.POST['anticipo'])))
        pedido.save()

    return redirect('/agenda/')

def renderSubidorImagenes(request):
    return render(request, 'subidorimagenes.html')
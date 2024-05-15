from django import forms
from .models import Cliente, Pedido
from bootstrap_datepicker_plus import DatePickerInput


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_cliente', 'celular']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'fecha_entrega', 'fecha_entregado', 'descripcion', 'tamano', 'costo', 'anticipo', 'restante', 'estatus', 'imagen']

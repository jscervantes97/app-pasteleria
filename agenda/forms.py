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


class CrearActualizarPedidoForm(forms.Form):
    fecha_entrega = forms.DateField(
        widget=DatePickerInput(format='%Y-%m-%d', attrs={'style': 'width: 100%;', 'class': 'form-control'})
    )
    descripcion = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'style': 'width: 100%;', 'class': 'form-control'}))
    tamano = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'style': 'width: 100%;', 'class': 'form-control'}))
    costo = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'style': 'width: 100%;', 'class': 'form-control'}))
    anticipo = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'style': 'width: 100%;', 'class': 'form-control'}))
    nombre_cliente = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'style': 'width: 100%;', 'class': 'form-control'}))
    celular = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'style': 'width: 100%;', 'class': 'form-control'}))
    imagen = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        costo = cleaned_data.get('costo')
        anticipo = cleaned_data.get('anticipo')

        if costo is not None and anticipo is not None:
            if anticipo > costo:
                self.add_error('anticipo', 'El anticipo no puede ser mayor que el costo.')
        
        return cleaned_data
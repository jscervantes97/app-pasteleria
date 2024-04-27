import django_filters
from .models import Pedido

class PedidoFilter(django_filters.FilterSet):
    nombre_cliente = django_filters.CharFilter(field_name='cliente__nombre_cliente', lookup_expr='icontains')

    class Meta:
        model = Pedido
        fields = ['nombre_cliente']
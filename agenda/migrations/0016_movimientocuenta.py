# Regresa el desglose por movimiento (fecha/tipo/descripcion/monto), ahora
# ligado a la Cuenta de su mes. Los montos que ya se habian capturado a mano
# por mes se convierten en un movimiento "Saldo capturado antes del desglose"
# para que los totales del mes no cambien.

import datetime

import django.db.models.deletion
from django.db import migrations, models

DESCRIPCION_SALDO_PREVIO = 'Saldo capturado antes del desglose'


def pasar_saldos_a_movimientos(apps, schema_editor):
    Cuenta = apps.get_model('agenda', 'Cuenta')
    MovimientoCuenta = apps.get_model('agenda', 'MovimientoCuenta')

    for cuenta in Cuenta.objects.all():
        fecha = datetime.date(cuenta.anio, cuenta.mes, 1)
        if cuenta.ingreso:
            MovimientoCuenta.objects.create(cuenta=cuenta, fecha=fecha, tipo='ingreso', descripcion=DESCRIPCION_SALDO_PREVIO, monto=cuenta.ingreso)
        if cuenta.gasto:
            MovimientoCuenta.objects.create(cuenta=cuenta, fecha=fecha, tipo='gasto', descripcion=DESCRIPCION_SALDO_PREVIO, monto=cuenta.gasto)


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0015_cuenta_por_mes'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoCuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('tipo', models.CharField(choices=[('ingreso', 'Ingreso'), ('gasto', 'Gasto')], max_length=10)),
                ('descripcion', models.CharField(blank=True, default='', max_length=300)),
                ('monto', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimientos', to='agenda.cuenta')),
            ],
            options={
                'ordering': ['fecha', 'id'],
            },
        ),
        migrations.RunPython(pasar_saldos_a_movimientos, migrations.RunPython.noop),
    ]

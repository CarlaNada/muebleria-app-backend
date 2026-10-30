from rest_framework import serializers

from .models import Pedido, ItemPedido, Pago, Envio


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'id',
            'cliente',
            'estado',
            'fecha_creacion',
        ]
        read_only_fields = [
            'id',
            'cliente',
            'estado',
            'fecha_creacion',
        ]


class ItemPedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemPedido
        fields = [
            'id',
            'pedido',
            'producto',
            'cantidad',
            'precio_unitario',
        ]
        read_only_fields = [
            'id',
            'precio_unitario',
        ]

class PagoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pago
        fields = [
            'id',
            'pedido',
            'monto',
            'metodo',
            'estado',
            'fecha_creacion',
        ]
        read_only_fields = [
            'id',
            'estado',
            'fecha_creacion',
        ]

class EnvioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Envio
        fields = [
            'id',
            'pedido',
            'direccion',
            'estado',
            'fecha_envio',
            'fecha_entrega',
        ]
        read_only_fields = [
            'id',
            'estado',
            'fecha_envio',
            'fecha_entrega',
        ]
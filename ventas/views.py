from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from clientes.models import Cliente

from .models import Pedido, ItemPedido, Pago, Envio
from .serializers import (
    PedidoSerializer,
    PedidoListSerializer,
    ItemPedidoSerializer,
    PagoSerializer,
    EnvioSerializer,
)

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PedidoListSerializer

        return PedidoSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]

        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Pedido.objects.all()

        return Pedido.objects.filter(
            cliente__usuario=self.request.user
        )


    def perform_create(self, serializer):
        try:
            cliente = Cliente.objects.get(
                usuario=self.request.user
            )
        except Cliente.DoesNotExist:
            raise ValidationError({
                'cliente': 'Primero debes crear un perfil de cliente.'
            })

        serializer.save(cliente=cliente)

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        pedido = self.get_object()

        if pedido.estado != 'pendiente':
            raise ValidationError({
                'estado': 'Solo se pueden cancelar pedidos pendientes.'
            })

        if pedido.pagos.filter(estado='aprobado').exists():
            raise ValidationError({
                'pedido': 'No se puede cancelar un pedido con pagos aprobados.'
            })

        pedido.estado = 'cancelado'
        pedido.save(update_fields=['estado'])

        return Response(
            {'mensaje': 'Pedido cancelado correctamente.'},
            status=status.HTTP_200_OK
        )

class ItemPedidoViewSet(viewsets.ModelViewSet):
    serializer_class = ItemPedidoSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]

        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ItemPedido.objects.all()

        return ItemPedido.objects.filter(
            pedido__cliente__usuario=self.request.user
        )

    def perform_create(self, serializer):
        pedido = serializer.validated_data['pedido']
        producto = serializer.validated_data['producto']
        cantidad = serializer.validated_data['cantidad']

        if not self.request.user.is_staff and pedido.cliente.usuario_id != self.request.user.id:
            raise PermissionDenied(
                'No puedes agregar productos a pedidos de otros clientes.'
            )

        if pedido.estado != 'pendiente':
            raise ValidationError({
                'pedido': 'Solo puedes agregar productos a pedidos pendientes.'
            })

        if not producto.activo:
            raise ValidationError({
                'producto': 'El producto no está disponible.'
            })

        if cantidad > producto.stock:
            raise ValidationError({
                'cantidad': 'No hay suficiente stock disponible.'
            })

        serializer.save(precio_unitario=producto.precio)

    def perform_update(self, serializer):
        pedido = serializer.validated_data.get(
            'pedido', serializer.instance.pedido
        )
        producto = serializer.validated_data.get(
            'producto', serializer.instance.producto
        )

        if pedido.estado != 'pendiente':
            raise ValidationError({
                'pedido': 'No puedes modificar un pedido que no está pendiente.'
            })

        if 'producto' in serializer.validated_data:
            serializer.save(precio_unitario=producto.precio)
        else:
            serializer.save()

    def perform_destroy(self, instance):
        if instance.pedido.estado != 'pendiente':
            raise ValidationError({
                'pedido': 'No puedes eliminar ítems de un pedido que no está pendiente.'
            })

        instance.delete()

class PagoViewSet(viewsets.ModelViewSet):
    serializer_class = PagoSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]

        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Pago.objects.all()

        return Pago.objects.filter(
            pedido__cliente__usuario=self.request.user
        )

    def perform_create(self, serializer):
        pedido = serializer.validated_data['pedido']

        if pedido.estado == 'cancelado':
            raise ValidationError({
                'pedido': 'No se pueden registrar pagos de pedidos cancelados.'
            })

        serializer.save()

class EnvioViewSet(viewsets.ModelViewSet):
    serializer_class = EnvioSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]

        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Envio.objects.all()

        return Envio.objects.filter(
            pedido__cliente__usuario=self.request.user
        )

    def perform_create(self, serializer):
        pedido = serializer.validated_data['pedido']
        direccion = serializer.validated_data['direccion']

        if pedido.estado == 'cancelado':
            raise ValidationError({
                'pedido': 'No se pueden crear envíos para pedidos cancelados.'
            })

        if direccion.cliente_id != pedido.cliente_id:
            raise ValidationError({
                'direccion': 'La dirección no pertenece al cliente del pedido.'
            })

        if Envio.objects.filter(pedido=pedido).exists():
            raise ValidationError({
                'pedido': 'Este pedido ya tiene un envío.'
            })

        serializer.save()

    def perform_update(self, serializer):
        pedido = serializer.validated_data.get(
            'pedido', serializer.instance.pedido
        )
        direccion = serializer.validated_data.get(
            'direccion', serializer.instance.direccion
        )

        if direccion.cliente_id != pedido.cliente_id:
            raise ValidationError({
                'direccion': 'La dirección no pertenece al cliente del pedido.'
            })

        if pedido.estado == 'cancelado':
            raise ValidationError({
                'pedido': 'No se puede modificar el envío de un pedido cancelado.'
            })

        if Envio.objects.exclude(pk=serializer.instance.pk).filter(pedido=pedido).exists():
            raise ValidationError({
                'pedido': 'Este pedido ya tiene un envío.'
            })

        serializer.save()
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator


class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.PROTECT,
        related_name='pedidos',
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente',
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'

    def __str__(self):
        return f'Pedido {self.id} - {self.cliente}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='items',
    )
    producto = models.ForeignKey(
        'catalogo.Producto',
        on_delete=models.PROTECT,
        related_name='items_pedido',
    )
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'ítem de pedido'
        verbose_name_plural = 'ítems de pedidos'

    def __str__(self):
        return f'{self.producto} - Cantidad: {self.cantidad}'


class Pago(models.Model):
    METODOS = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'),
    ]

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='pagos',
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    metodo = models.CharField(
        max_length=20,
        choices=METODOS,
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente',
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'pago'
        verbose_name_plural = 'pagos'

    def __str__(self):
        return f'Pago {self.id} - Pedido {self.pedido.id}'


class Envio(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='envio',
    )
    direccion = models.ForeignKey(
        'clientes.Direccion',
        on_delete=models.PROTECT,
        related_name='envios',
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente',
    )
    fecha_envio = models.DateTimeField(
        null=True,
        blank=True,
    )
    fecha_entrega = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'envío'
        verbose_name_plural = 'envíos'

    def __str__(self):
        return f'Envio {self.id} - Pedido {self.pedido.id}'
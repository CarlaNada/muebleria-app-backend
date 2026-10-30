from django.contrib import admin

from .models import Pedido, ItemPedido, Pago, Envio


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'estado', 'fecha_creacion']
    search_fields = ['cliente__usuario__username']
    list_filter = ['estado', 'fecha_creacion']
    ordering = ['-fecha_creacion']


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'producto', 'cantidad', 'precio_unitario']
    search_fields = ['producto__nombre']
    list_filter = ['producto']
    ordering = ['id']


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'monto', 'metodo', 'estado', 'fecha_creacion']
    search_fields = ['pedido__id']
    list_filter = ['metodo', 'estado']
    ordering = ['-fecha_creacion']


@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'direccion', 'estado', 'fecha_envio', 'fecha_entrega']
    search_fields = ['pedido__id', 'direccion__ciudad']
    list_filter = ['estado']
    ordering = ['id']
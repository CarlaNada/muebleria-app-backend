from django.contrib import admin

from .models import Cliente, Direccion


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'telefono', 'fecha_creacion']
    search_fields = ['usuario__username', 'telefono']
    list_filter = ['fecha_creacion']
    ordering = ['id']


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'calle', 'numero', 'ciudad', 'provincia']
    search_fields = ['calle', 'ciudad', 'provincia']
    list_filter = ['ciudad', 'provincia']
    ordering = ['id']
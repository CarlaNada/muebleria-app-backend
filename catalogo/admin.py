from django.contrib import admin

from .models import Categoria, Material, Producto, ProductoMaterial


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa', 'fecha_creacion')
    list_filter = ('activa',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)


class ProductoMaterialInline(admin.TabularInline):
    model = ProductoMaterial
    extra = 1
    autocomplete_fields = ('material',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'activo')
    list_filter = ('activo', 'categoria')
    search_fields = ('nombre', 'descripcion', 'categoria__nombre', 'materiales__nombre')
    ordering = ('nombre',)
    list_select_related = ('categoria',)
    list_editable = ('precio', 'stock', 'activo')
    inlines = (ProductoMaterialInline,)


@admin.register(ProductoMaterial)
class ProductoMaterialAdmin(admin.ModelAdmin):
    list_display = ('producto', 'material')
    list_filter = ('material',)
    search_fields = ('producto__nombre', 'material__nombre')
    ordering = ('producto__nombre', 'material__nombre')
    list_select_related = ('producto', 'material')
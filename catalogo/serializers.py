from rest_framework import serializers

from .models import Categoria, Material, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = (
            'id',
            'nombre',
            'descripcion',
            'activa',
            'fecha_creacion',
        )
        read_only_fields = ('id', 'fecha_creacion')


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = (
            'id',
            'nombre',
            'descripcion',
            'activo',
            'fecha_creacion',
        )
        read_only_fields = ('id', 'fecha_creacion')


class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        source='categoria',
        queryset=Categoria.objects.all(),
        write_only=True,
    )

    materiales = MaterialSerializer(many=True, read_only=True)
    materiales_ids = serializers.PrimaryKeyRelatedField(
        source='materiales',
        queryset=Material.objects.all(),
        many=True,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre',
            'descripcion',
            'categoria',
            'categoria_id',
            'materiales',
            'materiales_ids',
            'precio',
            'stock',
            'activo',
            'fecha_creacion',
            'fecha_actualizacion',
        )
        read_only_fields = (
            'id',
            'fecha_creacion',
            'fecha_actualizacion',
        )

class ProductoListaSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    materiales = MaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre',
            'descripcion',
            'categoria',
            'materiales',
            'precio',
            'stock',
            'activo',
            'destacado',
            'fecha_creacion',
            'fecha_actualizacion',
        )
        read_only_fields = fields
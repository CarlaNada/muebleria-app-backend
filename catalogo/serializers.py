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
    materiales = serializers.PrimaryKeyRelatedField(
    queryset=Material.objects.all(),
    many=True,
    required=False,
    )

    def create(self, validated_data):
        materiales = validated_data.pop('materiales', [])
        producto = Producto.objects.create(**validated_data)
        producto.materiales.set(materiales)
        return producto

    def update(self, instance, validated_data):
        materiales = validated_data.pop('materiales', None)
        producto = super().update(instance, validated_data)

        if materiales is not None:
            producto.materiales.set(materiales)

        return producto
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

class ProductoResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre',
            'precio',
            'stock',
            'activo',
        )
        read_only_fields = fields

class CategoriaListaSerializer(serializers.ModelSerializer):
    productos = ProductoResumenSerializer(many=True, read_only=True)

    class Meta:
        model = Categoria
        fields = (
            'id',
            'nombre',
            'descripcion',
            'activa',
            'fecha_creacion',
            'productos',
        )
        read_only_fields = fields
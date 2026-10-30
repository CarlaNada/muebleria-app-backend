from rest_framework import serializers

from .models import Cliente, Direccion


class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = [
            'id',
            'usuario',
            'telefono',
            'fecha_creacion',
        ]
        read_only_fields = [
            'id',
            'usuario',
            'fecha_creacion',
        ]


class DireccionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Direccion
        fields = [
            'id',
            'cliente',
            'calle',
            'numero',
            'ciudad',
            'provincia',
            'codigo_postal',
        ]
        read_only_fields = [
            'id',
            'cliente',
        ]
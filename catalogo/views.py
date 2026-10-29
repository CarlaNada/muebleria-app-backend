from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Categoria, Material, Producto
from .serializers import (
    CategoriaSerializer,
    MaterialSerializer,
    ProductoListaSerializer,
    ProductoSerializer,
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('nombre', 'descripcion')
    ordering_fields = ('nombre', 'fecha_creacion')
    ordering = ('nombre',)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('nombre', 'descripcion')
    ordering_fields = ('nombre', 'fecha_creacion')
    ordering = ('nombre',)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = (
        Producto.objects
        .select_related('categoria')
        .prefetch_related('materiales')
        .all()
    )
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = (
        'nombre',
        'descripcion',
        'categoria__nombre',
        'materiales__nombre',
    )
    ordering_fields = ('nombre', 'precio', 'stock', 'fecha_creacion')
    ordering = ('nombre',)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductoListaSerializer
        return ProductoSerializer

    @action(detail=False, methods=('get',))
    def destacados(self, request):
        productos = self.filter_queryset(
            self.get_queryset().filter(destacado=True, activo=True)
        )
        pagina = self.paginate_queryset(productos)

        if pagina is not None:
            serializer = self.get_serializer(pagina, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=('get',))
    def disponibles(self, request):
        productos = self.filter_queryset(
            self.get_queryset().filter(stock__gt=0, activo=True)
        )
        pagina = self.paginate_queryset(productos)

        if pagina is not None:
            serializer = self.get_serializer(pagina, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)
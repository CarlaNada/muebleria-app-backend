from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

    def __str__(self):
        return self.nombre


class Material(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'material'
        verbose_name_plural = 'materiales'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    destacado = models.BooleanField(default=False)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
    )
    materiales = models.ManyToManyField(
        Material,
        through='ProductoMaterial',
        related_name='productos',
        blank=True,
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio__gte=0),
                name='catalogo_precio_no_negativo',
            ),
        ]

    def __str__(self):
        return self.nombre


class ProductoMaterial(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='materiales_asociados',
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name='productos_asociados',
    )

    class Meta:
        ordering = ['producto', 'material']
        verbose_name = 'material de producto'
        verbose_name_plural = 'materiales de productos'
        constraints = [
            models.UniqueConstraint(
                fields=['producto', 'material'],
                name='producto_material_unico',
            ),
        ]

    def __str__(self):
        return f'{self.producto} - {self.material}'
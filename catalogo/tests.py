from django.contrib.auth import get_user_model
from decimal import Decimal

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Categoria, Producto


class CatalogoPermisosTest(APITestCase):

    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre='Mesas'
        )

        self.producto = Producto.objects.create(
            nombre='Mesa de prueba',
            categoria=self.categoria,
            precio=Decimal('85000.00'),
            stock=5
        )

    def test_visitante_puede_consultar_productos(self):
        respuesta = self.client.get('/api/catalogo/productos/')

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(respuesta.data['count'], 1)

    def test_visitante_no_puede_crear_producto(self):
        datos = {
            'nombre': 'Silla de prueba',
            'categoria': self.categoria.id,
            'precio': '35000.00',
            'stock': 3,
        }

        respuesta = self.client.post(
            '/api/catalogo/productos/',
            datos,
            format='json'
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(Producto.objects.count(), 1)

    def test_usuario_comun_no_puede_crear_producto(self):
        Usuario = get_user_model()

        usuario = Usuario.objects.create_user(
            username='cliente_prueba',
            password='password123',
            is_staff=False
        )

        self.client.force_authenticate(user=usuario)

        datos = {
            'nombre': 'Silla de prueba',
            'categoria': self.categoria.id,
            'precio': '35000.00',
            'stock': 3,
        }

        respuesta = self.client.post(
            '/api/catalogo/productos/',
            datos,
            format='json'
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(Producto.objects.count(), 1)

    def test_administrador_puede_crear_producto(self):
        Usuario = get_user_model()

        administrador = Usuario.objects.create_user(
            username='admin_prueba',
            password='password123',
            is_staff=True
        )

        self.client.force_authenticate(user=administrador)

        datos = {
            'nombre': 'Silla de prueba',
            'categoria': self.categoria.id,
            'precio': '35000.00',
            'stock': 3,
        }

        respuesta = self.client.post(
            '/api/catalogo/productos/',
            datos,
            format='json'
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(Producto.objects.count(), 2)

        self.assertTrue(
            Producto.objects.filter(
                nombre='Silla de prueba'
            ).exists()
        )
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from clientes.models import Cliente
from .models import Pedido


class PedidoPermisosTest(APITestCase):

    def setUp(self):
        Usuario = get_user_model()

        self.usuario1 = Usuario.objects.create_user(
            username='usuario1'
        )
        self.usuario2 = Usuario.objects.create_user(
            username='usuario2'
        )

        self.cliente1 = Cliente.objects.create(
            usuario=self.usuario1
        )
        self.cliente2 = Cliente.objects.create(
            usuario=self.usuario2
        )

        self.pedido1 = Pedido.objects.create(
            cliente=self.cliente1
        )
        self.pedido2 = Pedido.objects.create(
            cliente=self.cliente2
        )

        self.client.force_authenticate(user=self.usuario1)

    def test_cliente_solo_ve_sus_pedidos(self):
        respuesta = self.client.get('/api/ventas/pedidos/')

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['count'], 1)
        self.assertEqual(
            respuesta.data['results'][0]['id'],
            self.pedido1.id
        )

    def test_cliente_no_puede_cancelar_pedido_ajeno(self):
        respuesta = self.client.post(
            f'/api/ventas/pedidos/{self.pedido2.id}/cancelar/'
        )

        self.assertEqual(respuesta.status_code, 404)

        self.pedido2.refresh_from_db()
        self.assertEqual(self.pedido2.estado, 'pendiente')
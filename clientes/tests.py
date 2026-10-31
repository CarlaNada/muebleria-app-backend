from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Cliente, Direccion


class ClientePermisosTest(APITestCase):

    def setUp(self):
        Usuario = get_user_model()

        self.usuario1 = Usuario.objects.create_user(
            username='usuario1'
        )
        self.usuario2 = Usuario.objects.create_user(
            username='usuario2'
        )

        self.cliente1 = Cliente.objects.create(
            usuario=self.usuario1,
            telefono='3584000001'
        )

        self.cliente2 = Cliente.objects.create(
            usuario=self.usuario2,
            telefono='3584000002'
        )

        self.direccion2 = Direccion.objects.create(
            cliente=self.cliente2,
            calle='San Martin',
            numero='450',
            ciudad='Rio Cuarto',
            provincia='Cordoba',
            codigo_postal='5800'
        )

        self.client.force_authenticate(user=self.usuario1)

    def test_cliente_ve_sus_datos(self):
        respuesta = self.client.get('/api/clientes/')

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['count'], 1)
        self.assertEqual(
            respuesta.data['results'][0]['id'],
            self.cliente1.id
        )

    def test_cliente_no_ve_otro_cliente(self):
        respuesta = self.client.get(
            f'/api/clientes/{self.cliente2.id}/'
        )

        self.assertEqual(respuesta.status_code, 404)

    def test_cliente_no_ve_direccion_ajena(self):
        respuesta = self.client.get(
            f'/api/direcciones/{self.direccion2.id}/'
        )

        self.assertEqual(respuesta.status_code, 404)



    def test_cliente_no_puede_editar_otro_cliente(self):
        respuesta = self.client.patch(
            f'/api/clientes/{self.cliente2.id}/',
            {'telefono': '3584999999'},
            format='json'
        )

        self.assertEqual(respuesta.status_code, 404)

        self.cliente2.refresh_from_db()
        self.assertEqual(self.cliente2.telefono, '3584000002')

    def test_cliente_no_puede_eliminar_direccion_ajena(self):
        respuesta = self.client.delete(
            f'/api/direcciones/{self.direccion2.id}/'
        )

        self.assertEqual(respuesta.status_code, 404)

        self.assertTrue(
            Direccion.objects.filter(
                id=self.direccion2.id
            ).exists()
        )
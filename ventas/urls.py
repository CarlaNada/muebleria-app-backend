from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PedidoViewSet,
    ItemPedidoViewSet,
    PagoViewSet,
    EnvioViewSet,
)


router = DefaultRouter()

router.register('pedidos', PedidoViewSet, basename='pedido')
router.register('items', ItemPedidoViewSet, basename='itempedido')
router.register('pagos', PagoViewSet, basename='pago')
router.register('envios', EnvioViewSet, basename='envio')


urlpatterns = [
    path('', include(router.urls)),
]
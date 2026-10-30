from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClienteViewSet, DireccionViewSet


router = DefaultRouter()

router.register('clientes', ClienteViewSet, basename='cliente')
router.register('direcciones', DireccionViewSet, basename='direccion')


urlpatterns = [
    path('', include(router.urls)),
]
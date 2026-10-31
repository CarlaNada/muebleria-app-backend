from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import Cliente, Direccion
from .serializers import ClienteSerializer, DireccionSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Cliente.objects.all()

        return Cliente.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        if Cliente.objects.filter(usuario=self.request.user).exists():
            raise ValidationError({
                'usuario': 'Ya existe un cliente para este usuario.'
            })

        serializer.save(usuario=self.request.user)


class DireccionViewSet(viewsets.ModelViewSet):
    serializer_class = DireccionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Direccion.objects.all()

        return Direccion.objects.filter(
            cliente__usuario=self.request.user
        )

    def perform_create(self, serializer):
        try:
            cliente = Cliente.objects.get(usuario=self.request.user)
        except Cliente.DoesNotExist:
            raise ValidationError({
                'cliente': 'Primero debes crear un perfil de cliente.'
            })

        serializer.save(cliente=cliente)
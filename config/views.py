from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuario_actual(request):
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
    })

def bienvenida(request):
    return render(request, 'bienvenida.html')
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.service_address.models import ServiceAddress
from apps.service_address.serializers import ServiceAddressSerializer
from apps.users.permissions import IsPatient

class ServiceAddressViewSet(viewsets.ModelViewSet):
    queryset = ServiceAddress.objects.all()
    serializer_class = ServiceAddressSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPatient | IsAdminUser]

    def get_queryset(self):
        # Filtrar las direcciones por el usuario autenticado
        user = self.request.user
        return ServiceAddress.objects.filter(patient=user)
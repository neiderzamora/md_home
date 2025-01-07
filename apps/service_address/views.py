from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import ValidationError

from apps.service_address.models import ServiceAddress
from apps.service_address.serializers import ServiceAddressSerializer
from apps.users.permissions import IsPatient
from django.contrib.auth.models import Group

class ServiceAddressViewSet(viewsets.ModelViewSet):
    queryset = ServiceAddress.objects.all()
    serializer_class = ServiceAddressSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPatient | IsAdminUser]

    def get_queryset(self):
        # Filtrar las direcciones por el usuario autenticado
        user = self.request.user
        if user.groups.filter(name='Patients').exists():
            return ServiceAddress.objects.filter(patient=user.patientuser)
        else:
            raise ValidationError("El usuario autenticado no es un paciente.")

    def perform_create(self, serializer):
        user = self.request.user
        if user.groups.filter(name='Patients').exists():
            serializer.save(patient=user.patientuser)
        else:
            raise ValidationError("El usuario autenticado no es un paciente.")
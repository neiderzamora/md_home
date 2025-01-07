from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import ValidationError

from apps.vehicle.models import Vehicle
from apps.vehicle.serializers import VehicleSerializer
from apps.users.permissions import IsDoctor

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor | IsAdminUser]

    def get_queryset(self):
        # Filtrar los vehículos por el usuario autenticado
        user = self.request.user
        if user.groups.filter(name='Doctors').exists():
            return Vehicle.objects.filter(doctor_user=user.doctoruser)
        else:
            raise ValidationError("El usuario autenticado no es un doctor.")

    def perform_create(self, serializer):
        user = self.request.user
        if user.groups.filter(name='Doctors').exists():
            serializer.save(doctor_user=user.doctoruser)
        else:
            raise ValidationError("El usuario autenticado no es un doctor.")
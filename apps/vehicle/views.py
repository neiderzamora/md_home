from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.users.permissions import CanEditDoctor
from apps.vehicle.models import Vehicle
from apps.vehicle.serializers import VehicleSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated, CanEditDoctor]

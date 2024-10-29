from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from apps.users.models import PatientUser, DoctorUser
from apps.users.serializers import PatientUserSerializer, DoctorUserSerializer

class PatientUserViewSet(viewsets.ModelViewSet):
    queryset = PatientUser.objects.all()
    serializer_class = PatientUserSerializer
    permission_classes = []

class DoctorUserViewSet(viewsets.ModelViewSet):
    queryset = DoctorUser.objects.all()
    serializer_class = DoctorUserSerializer
    permission_classes = []

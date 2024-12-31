from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.service_end.models import ServiceEnd
from apps.users.models import PatientUser, DoctorUser
from apps.service_request.models import PatientServiceRequest, DoctorServiceResponse

from apps.service_request.serializers import PatientServiceRequestSerializer, DoctorServiceResponseSerializer, DoctorServiceResponseCreateSerializer, ServiceEndSerializer

from apps.users.permissions import IsPatient, IsDoctor

""" Patient view """
class PatientServiceRequestCreateView(generics.CreateAPIView):
    queryset = PatientServiceRequest.objects.all()
    serializer_class = PatientServiceRequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPatient | IsAdminUser]

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'patientuser'):
            raise serializers.ValidationError({'error': 'El usuario autenticado no es un paciente'})
        serializer.save(patient=self.request.user.patientuser)

class PatientServiceRequestListView(generics.ListAPIView):
    serializer_class = PatientServiceRequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPatient | IsAdminUser]

    def get_queryset(self):
        return PatientServiceRequest.objects.filter(patient=self.request.user.patientuser)

class PatientServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientServiceRequest.objects.all()
    serializer_class = PatientServiceRequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPatient | IsAdminUser]

    def get_queryset(self):
        return PatientServiceRequest.objects.filter(patient=self.request.user.patientuser)

    def perform_destroy(self, instance):
        if instance.status != 'PD':
            raise serializers.ValidationError({'error': 'No se puede eliminar una solicitud que ya ha sido aceptada por un doctor'})
        instance.delete()
    
    
""" Doctor view """
class DoctorServiceResponseCreateView(generics.CreateAPIView):
    queryset = DoctorServiceResponse.objects.all()
    serializer_class = DoctorServiceResponseCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor | IsAdminUser]

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'doctoruser'):
            return Response({'error': 'El usuario autenticado no es un doctor'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service_request = PatientServiceRequest.objects.get(pk=self.kwargs['pk'])
        except PatientServiceRequest.DoesNotExist:
            return Response({'error': 'La solicitud de servicio no existe'}, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar si ya existe una respuesta para esta solicitud
        existing_response = DoctorServiceResponse.objects.filter(service_request=service_request).first()
        if existing_response:
            return Response({'error': 'Ya existe una respuesta para esta solicitud de servicio'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(doctor=self.request.user.doctoruser, service_request=service_request)
        service_request.status = 'AC'
        service_request.save()

class DoctorServiceResponseListView(generics.ListAPIView):
    serializer_class = DoctorServiceResponseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor | IsAdminUser]

    def get_queryset(self):
        return DoctorServiceResponse.objects.filter(doctor=self.request.user)

class DoctorMarkArrivalView(generics.UpdateAPIView):
    queryset = DoctorServiceResponse.objects.all()
    serializer_class = DoctorServiceResponseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor | IsAdminUser]

    def patch(self, request, *args, **kwargs):
        try:
            service_request = PatientServiceRequest.objects.get(pk=self.kwargs['pk'])
        except PatientServiceRequest.DoesNotExist:
            return Response({'error': 'No PatientServiceRequest matches the given query.'}, status=status.HTTP_404_NOT_FOUND)
        
        if not hasattr(request.user, 'doctoruser'):
            return Response({'error': 'El usuario autenticado no es un doctor'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            instance = DoctorServiceResponse.objects.get(service_request=service_request)
        except DoctorServiceResponse.DoesNotExist:
            return Response({'error': 'No DoctorServiceResponse matches the given query.'}, status=status.HTTP_404_NOT_FOUND)
        
        instance.status = 'LG'
        instance.save()
        service_request.status = 'LG'
        service_request.save()
        return Response({'status': 'Llegue'}, status=status.HTTP_200_OK)

class DoctorServiceResponseDetailView(generics.RetrieveAPIView):
    queryset = DoctorServiceResponse.objects.all()
    serializer_class = DoctorServiceResponseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor | IsAdminUser]

    def get_queryset(self):
        return DoctorServiceResponse.objects.filter(doctor=self.request.user)

""" Service_end view """
class ServiceEndCreateView(generics.CreateAPIView):
    queryset = ServiceEnd.objects.all()
    serializer_class = ServiceEndSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor | IsAdminUser]

    def perform_create(self, serializer):
        try:
            service_request = PatientServiceRequest.objects.get(pk=self.kwargs['pk'])
        except PatientServiceRequest.DoesNotExist:
            return Response({'error': 'No PatientServiceRequest matches the given query.'}, status=status.HTTP_404_NOT_FOUND)
        
        service_end = serializer.save(service_request=service_request)
        
        # Actualizar el estado de DoctorServiceResponse y PatientServiceRequest a "completado"
        service_response = DoctorServiceResponse.objects.get(service_request=service_request)
        service_response.status = 'CP'
        service_response.save()
        
        service_request.status = 'CP'
        service_request.save()
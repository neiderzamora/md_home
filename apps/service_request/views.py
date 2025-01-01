from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from apps.service_end.models import ServiceEnd
from apps.users.models import PatientUser, DoctorUser
from apps.service_request.models import PatientServiceRequest, DoctorServiceResponse, ServiceRequestDetail

from apps.service_request.serializers import PatientServiceRequestSerializer, DoctorServiceResponseSerializer, DoctorServiceResponseCreateSerializer, ServiceEndSerializer, ServiceRequestDetailSerializer

from apps.users.permissions import IsPatient, IsDoctor
from apps.service_request.filters import PatientServiceRequestFilter, DoctorServiceResponseFilter

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = PatientServiceRequestFilter
    pagination_class = PageNumberPagination

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
        if instance.status != 'PENDIENTE':
            raise serializers.ValidationError({'error': 'No se puede eliminar una solicitud que ya ha sido aceptada por un doctor'})
        instance.delete()

class AllServiceRequestDetailView(generics.RetrieveAPIView):
    queryset = PatientServiceRequest.objects.all()
    serializer_class = PatientServiceRequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor | IsAdminUser]
    
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
        service_request.status = 'ACEPTADA Y EN CAMINO'
        service_request.save()
        
        return Response({'status': 'La solicitud de servicio ha sido aceptada'}, status=status.HTTP_201_CREATED)

class DoctorServiceResponseListView(generics.ListAPIView):
    serializer_class = DoctorServiceResponseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor | IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DoctorServiceResponseFilter
    pagination_class = PageNumberPagination

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
        
        #instance.status = 'LG'
        #instance.save()
        service_request.status = 'LLEGADA AL DOMICILIO'
        service_request.save()
        return Response({'status': f'El doctor {instance.doctor.first_name} {instance.doctor.last_name} ha llegado a la dirección'}, status=status.HTTP_200_OK)

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
        
        # Actualizar el estado de PatientServiceRequest a "completado"
        service_response = DoctorServiceResponse.objects.get(service_request=service_request)
        
        service_request.status = 'COMPLETADA'
        service_request.save()
        
        # Crear una instancia de ServiceRequestDetail
        doctor_service_response = DoctorServiceResponse.objects.get(service_request=service_request)
        ServiceRequestDetail.objects.create(
            patient_service_request=service_request,
            doctor_service_response=doctor_service_response,
            service_end=service_end,
            location=service_request.location,
            patient=service_request.patient,
            doctor=doctor_service_response.doctor
        )

""" ServiceRequestDetail view """
class PatientServiceRequestDListView(generics.ListAPIView):
    serializer_class = ServiceRequestDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPatient | IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return ServiceRequestDetail.objects.filter(patient=self.request.user.patientuser)

class PatientServiceRequestDView(generics.RetrieveAPIView):
    serializer_class = ServiceRequestDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPatient | IsAdminUser]

    def get_queryset(self):
        return ServiceRequestDetail.objects.filter(patient=self.request.user.patientuser)

class DoctorServiceResponseDListView(generics.ListAPIView):
    serializer_class = ServiceRequestDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor | IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return ServiceRequestDetail.objects.filter(doctor=self.request.user.doctoruser)

class DoctorServiceResponseDView(generics.RetrieveAPIView):
    serializer_class = ServiceRequestDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor | IsAdminUser]

    def get_queryset(self):
        return ServiceRequestDetail.objects.filter(doctor=self.request.user.doctoruser)
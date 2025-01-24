from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from datetime import timedelta
import threading

from apps.service_end.models import ServiceEnd
from apps.users.models import PatientUser, DoctorUser
from apps.service_request.models import PatientServiceRequest, DoctorServiceResponse, ServiceRequestDetail

from apps.service_request.serializers import PatientServiceRequestSerializer, DoctorServiceResponseSerializer, DoctorServiceResponseCreateSerializer, ServiceEndSerializer, ServiceRequestDetailSerializer

from apps.users.permissions import IsPatient, IsDoctor
from apps.service_request.utils.email_templates import service_request_accepted_email, doctor_arrival_email, service_end_email
from apps.service_request.filters import PatientServiceRequestFilter, DoctorServiceResponseFilter
from django.core.mail import send_mail
from django.conf import settings

""" Patient view """
def delete_unaccepted_request(service_request_id):
    try:
        service_request = PatientServiceRequest.objects.get(id=service_request_id, status='PENDIENTE')
        service_request.delete()
    except PatientServiceRequest.DoesNotExist:
        pass

class PatientServiceRequestCreateView(generics.CreateAPIView):
    queryset = PatientServiceRequest.objects.all()
    serializer_class = PatientServiceRequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPatient | IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_request = serializer.save(patient=self.request.user.patientuser)
        
        # Programar la eliminación de la solicitud si no es aceptada en 30 minutos
        timer = threading.Timer(30 * 60, delete_unaccepted_request, [service_request.id])
        timer.start()
        
        headers = self.get_success_headers(serializer.data)
        return Response({
            'status': 'La solicitud de servicio ha sido creada',
            'message': 'Si la solicitud no es aceptada será eliminada en 30 minutos, vuelve a crear otra',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

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

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status': 'La solicitud de servicio ha sido actualizada',
            'message': 'La solicitud de servicio ha sido actualizada correctamente',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'PENDIENTE':
            return Response({'error': 'No se puede eliminar una solicitud que ya ha sido aceptada por un doctor'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response({
            'status': 'La solicitud de servicio ha sido eliminada',
            'message': 'La solicitud de servicio ha sido eliminada correctamente'
        }, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
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

    def create(self, request, *args, **kwargs):
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
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor_response = serializer.save(doctor=self.request.user.doctoruser, service_request=service_request)
        service_request.status = 'ACEPTADA Y EN CAMINO'
        service_request.save()
        
        # Obtener los componentes del correo desde el archivo de templates
        email_data = service_request_accepted_email(self.request.user.doctoruser, service_request.patient, service_request.id)
        
        try:
            send_mail(
                subject=email_data['subject'],
                message=email_data['message'],
                from_email=email_data['sender'],
                recipient_list=email_data['recipients'],
                fail_silently=False
            )
        except Exception as e:
            return Response(
                {'error': f'Error al enviar el correo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Obtener la respuesta completa usando el serializer detallado
        detailed_response = DoctorServiceResponseSerializer(doctor_response)
        
        response_data = {
            'status': 'La solicitud de servicio ha sido aceptada',
            'message': 'El doctor ha aceptado la solicitud y está en camino',
            'data': detailed_response.data
        }
        
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

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
        
        service_request.status = 'LLEGADA AL DOMICILIO'
        service_request.save()
        
        # Enviar correo al paciente confirmando la llegada del doctor
        email_data = doctor_arrival_email(request.user.doctoruser, service_request.patient)
        
        try:
            send_mail(
                subject=email_data['subject'],
                message=email_data['message'],
                from_email=email_data['sender'],
                recipient_list=email_data['recipients'],
                fail_silently=False
            )
        except Exception as e:
            return Response(
                {'error': f'Error al enviar el correo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({
            'status': 'El doctor ha llegado a la dirección',
            'message': f'El doctor {instance.doctor.first_name} {instance.doctor.last_name} ha llegado a la dirección',
            'data': DoctorServiceResponseSerializer(instance).data
        }, status=status.HTTP_200_OK)

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

    def create(self, request, *args, **kwargs):
        try:
            service_request = PatientServiceRequest.objects.get(pk=self.kwargs['pk'])
        except PatientServiceRequest.DoesNotExist:
            return Response({
                'error': 'Ninguna solicitud de servicio coincide con la consulta proporcionada.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Guardamos explícitamente service_request
        service_end = serializer.save(service_request=service_request)
        
        # Actualizamos el estado
        service_request.status = 'COMPLETADA'
        service_request.save()
        
        # Creamos ServiceRequestDetail
        doctor_service_response = DoctorServiceResponse.objects.get(service_request=service_request)
        ServiceRequestDetail.objects.create(
            patient_service_request=service_request,
            doctor_service_response=doctor_service_response,
            service_end=service_end,
            location=service_request.location,
            patient=service_request.patient,
            doctor=doctor_service_response.doctor
        )
        
        # Enviar correo al paciente confirmando la finalización del servicio
        email_data = service_end_email(doctor_service_response.doctor, service_request.patient)
        
        try:
            send_mail(
                subject=email_data['subject'],
                message=email_data['message'],
                from_email=email_data['sender'],
                recipient_list=email_data['recipients'],
                fail_silently=False
            )
        except Exception as e:
            return Response(
                {'error': f'Error al enviar el correo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        headers = self.get_success_headers(serializer.data)
        return Response({
            'status': 'El servicio ha sido completado',
            'message': 'El servicio ha sido completado y los detalles han sido guardados',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)      

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
    
""" Pending service request view """
class PendingServiceRequestListView(generics.ListAPIView):
    """
    Vista para listar todas las solicitudes de servicio con estado 'PENDIENTE'.
    """
    queryset = PatientServiceRequest.objects.filter(status='PENDIENTE')
    serializer_class = PatientServiceRequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor | IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PatientServiceRequestFilter
    pagination_class = PageNumberPagination
    
class PatientPendingServiceRequestListView(generics.ListAPIView):
    """
    Vista para listar todas las solicitudes de servicio del paciente autenticado con estado 'PENDIENTE'.
    """
    serializer_class = PatientServiceRequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PatientServiceRequestFilter
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return PatientServiceRequest.objects.filter(
            patient=self.request.user.patientuser,
            status='PENDIENTE'
        )

class PatientNonPendingServiceRequestListView(generics.ListAPIView):
    """
    Vista para listar todas las solicitudes de servicio del paciente autenticado con estados diferentes a 'PENDIENTE'.
    """
    serializer_class = PatientServiceRequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PatientServiceRequestFilter
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return PatientServiceRequest.objects.filter(
            patient=self.request.user.patientuser
        ).exclude(status__in=['PENDIENTE', 'COMPLETADA'])
        
        
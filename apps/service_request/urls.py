from django.urls import path
from .views import (
    PatientServiceRequestCreateView,
    PatientServiceRequestListView,
    PatientServiceRequestDetailView,
    #AllServiceRequestDetailView,
    
    DoctorServiceResponseCreateView,
    DoctorServiceResponseListView,
    DoctorServiceResponseDetailView,
    DoctorMarkArrivalView,
    ServiceEndCreateView,
    
    PatientServiceRequestDView,
    PatientServiceRequestDListView,
    DoctorServiceResponseDView,
    DoctorServiceResponseDListView,
    
    PendingServiceRequestListView,
    PatientPendingServiceRequestListView,
    PatientNonPendingServiceRequestListView,
)

urlpatterns = [
    # patient
    path('patient/service_request/new/', PatientServiceRequestCreateView.as_view(), name='create_service_request'),
    path('patient/service_request/list/', PatientServiceRequestListView.as_view(), name='list_service_requests'),
    path('patient/service_request/<uuid:pk>/', PatientServiceRequestDetailView.as_view(), name='detail_service_request'),
    
    # doctor
    path('doctor/service_request/<uuid:pk>/respond/', DoctorServiceResponseCreateView.as_view(), name='respond_service_request'),
    path('doctor/service_request/list/', DoctorServiceResponseListView.as_view(), name='list_doctor_service_responses'),
    path('doctor/service_request/<uuid:pk>/', DoctorServiceResponseDetailView.as_view(), name='detail_doctor_service_response'),
    path('doctor/service_request/<uuid:pk>/arrive/', DoctorMarkArrivalView.as_view(), name='mark_arrival'),
    
    # service_end
    path('service_end/<uuid:pk>/complete/', ServiceEndCreateView.as_view(), name='complete_service_end'),
    
    #path('service_request/<uuid:pk>/all/', AllServiceRequestDetailView.as_view(), name='all_service_request_detail'),
    
    path('patient/service_request/detail/', PatientServiceRequestDListView.as_view(), name='list_patient_service_request_detail'),
    path('patient/service_request/detail/<uuid:pk>/', PatientServiceRequestDView.as_view(), name='detail_patient_service_request_detail'),
    path('doctor/service_request/detail/', DoctorServiceResponseDListView.as_view(), name='list_doctor_service_response_detail'),
    path('doctor/service_request/detail/<uuid:pk>/', DoctorServiceResponseDView.as_view(), name='detail_doctor_service_response_detail'),
    
    path('service_requests/pending/', PendingServiceRequestListView.as_view(), name='list_pending_service_requests'),
    path('patient/service_request/pending/', 
        PatientPendingServiceRequestListView.as_view(), 
        name='patient_pending_service_requests'
    ),
    path(
        'patient/service_request/non_pending/',
        PatientNonPendingServiceRequestListView.as_view(),
        name='patient_non_pending_service_requests'
    ),
]
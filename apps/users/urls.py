from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import DoctorUserViewSet, PatientUserViewSet

router = DefaultRouter()
router.register(r'doctor', DoctorUserViewSet)
router.register(r'patient', PatientUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 
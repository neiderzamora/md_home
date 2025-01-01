from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import DoctorUserViewSet, PatientUserViewSet, ManualToken

router = DefaultRouter()
router.register(r'doctor', DoctorUserViewSet)
router.register(r'patient', PatientUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sign-in', ManualToken.as_view(), name='api-login'),
] 
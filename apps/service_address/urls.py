from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.service_address.views import ServiceAddressViewSet

router = DefaultRouter()
router.register(r'service-addresses', ServiceAddressViewSet, basename='service-address')

urlpatterns = [
    path('', include(router.urls)),
]
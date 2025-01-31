from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.service_end.views import CIE10CodeViewSet

router = DefaultRouter()
router.register(r'cie10-code', CIE10CodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
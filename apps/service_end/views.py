from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.users.permissions import IsDoctor
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from apps.service_end.models import CIE10Code
from apps.service_end.serializers import CIE10CodeSerializer

class CIE10Pagination(PageNumberPagination):
    page_size = 10  # Número de resultados por página
    page_size_query_param = 'page_size'
    max_page_size = 100

class CIE10CodeViewSet(viewsets.ModelViewSet):
    queryset = CIE10Code.objects.all()
    serializer_class = CIE10CodeSerializer
    pagination_class = CIE10Pagination

    def get_queryset(self):
        queryset = super().get_queryset()
        code = self.request.query_params.get('code', None)
        description = self.request.query_params.get('description', None)

        if code and description:
            queryset = queryset.filter(
                Q(code__icontains=code) | Q(description__icontains=description)
            )
        elif code:
            queryset = queryset.filter(code__icontains=code)
        elif description:
            queryset = queryset.filter(description__icontains=description)

        return queryset
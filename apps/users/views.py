from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from apps.users.models import PatientUser, DoctorUser
from apps.users.serializers import PatientUserSerializer, DoctorUserSerializer, LoginSerializer
from apps.users.permissions import IsPatient, IsDoctor

class BaseUserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action in ['destroy', 'update', 'partial_update', 'list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'No tiene permiso para eliminar usuarios'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    """ def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'No tiene permiso para eliminar usuarios'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs) """

class PatientUserViewSet(BaseUserViewSet):
    queryset = PatientUser.objects.all()
    serializer_class = PatientUserSerializer
    #permission_classes = [IsAuthenticated, IsPatient | IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'email']
    pagination_class = None

class DoctorUserViewSet(BaseUserViewSet):
    queryset = DoctorUser.objects.all()
    serializer_class = DoctorUserSerializer
    #permission_classes = [IsAuthenticated, IsDoctor | IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'email']
    pagination_class = None

class ManualToken(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    """ Token JWT """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response({'error': 'Credenciales invalidas'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({'access_token': access_token, 'refresh_token': refresh_token}, status=status.HTTP_200_OK)
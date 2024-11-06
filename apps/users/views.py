from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import PatientUser, DoctorUser
from apps.users.serializers import PatientUserSerializer, DoctorUserSerializer, LoginSerializer

class PatientUserViewSet(viewsets.ModelViewSet):
    queryset = PatientUser.objects.all()
    serializer_class = PatientUserSerializer
    permission_classes = [IsAuthenticated]

class DoctorUserViewSet(viewsets.ModelViewSet):
    queryset = DoctorUser.objects.all()
    serializer_class = DoctorUserSerializer
    permission_classes = []

class ManualTokenObtainView(APIView):
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

        return Response({'access_token': access_token}, status=status.HTTP_200_OK)
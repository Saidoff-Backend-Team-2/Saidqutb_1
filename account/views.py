from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from .models import User
from .serializers import UserRegisterSerializer, UserLoginRequestSerializer, UserUpdateSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import  generics
from rest_framework.permissions import IsAuthenticated


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = authenticate(username=data['username'], password=data['password'])

        if user:
            tokens = user.get_token()
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class UserAccountUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


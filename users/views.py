from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import ConfirmationCode
from .serializers import RegistrationSerializer, ConfirmSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(
            {"detail": "Пользователь зарегистрирован. Введите 6-значный код подтверждения."},
            status=status.HTTP_201_CREATED
        )

class ConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']

        try:
            conf = ConfirmationCode.objects.select_related('user').get(code=code, used=False)
        except ConfirmationCode.DoesNotExist:
            return Response({"detail": "Неверный код или уже использован."}, status=status.HTTP_400_BAD_REQUEST)

        user = conf.user
        user.is_active = True
        user.save()
        conf.used = True
        conf.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"detail": "Пользователь подтверждён.", "token": token.key})


class LoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.urls import reverse
from .serializers import UserRegistrationSerializer, CustomUserSerializer
from .gmail import send_mail
from django.http import HttpResponse
from .models import CustomUser


def confirm_email(request, token):
    user = CustomUser.objects.filter(confirmation_token=token).first()
    if user and not user.is_active:
        user.is_active = True
        user.confirmation_token = None
        user.save()
        return HttpResponse("Email successfully confirmed!")
    return HttpResponse("Invalid token or already confirmed.", status=400)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)  # Пользователь изначально не активен
        token = user.generate_confirmation_token()
        confirmation_url = self.request.build_absolute_uri(
            reverse("confirm-email", args=[token])
        )
        subject = "Подтверждение вашей электронной почты"
        message_text = f"Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить вашу электронную почту: {confirmation_url}"
        send_mail(subject, message_text, user.email)  # Отправляем письмо
        return Response(
            {
                "message": "Пожалуйста, проверьте вашу почту для подтверждения регистрации"
            },
            status=status.HTTP_201_CREATED,
        )


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

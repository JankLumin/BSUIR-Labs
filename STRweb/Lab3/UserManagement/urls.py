from django.urls import path
from .views import UserRegistrationView, confirm_email, UserProfileUpdateView


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("confirm-email/<str:token>/", confirm_email, name="confirm-email"),
    path(
        "profile/<int:pk>/",
        UserProfileUpdateView.as_view(),
        name="user_profile_update",
    ),
]

from django import forms
from UserManagement.models import CustomUser
from .models import Review


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Подтвердите пароль"
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number"]
        labels = {
            "username": "Имя пользователя",
            "email": "Электронная почта",
            "phone_number": "Номер телефона",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Пароли не совпадают.")


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "phone_number", "photo", "description"]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "phone_number": "Номер телефона",
            "photo": "Фотография",
            "description": "Описание",
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(
                choices=[(i, i) for i in range(1, 11)]
            ),
            "comment": forms.Textarea(attrs={"rows": 4}),
        }

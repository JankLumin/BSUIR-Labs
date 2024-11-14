from django.contrib.auth.models import AbstractUser, Group
from django.db import models
import uuid


class CustomUser(AbstractUser):
    ROLES = (
        ("superadmin", "Главный администратор"),
        ("admin", "Администратор"),
        ("employee", "Сотрудник"),
        ("client", "Клиент"),
    )
    role = models.CharField(
        max_length=10, choices=ROLES, default="client", verbose_name="Роль"
    )
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Номер телефона"
    )
    confirmation_token = models.CharField(max_length=36, blank=True, null=True)

    photo = models.ImageField(upload_to='employees/', verbose_name="Фото", blank=True, null=True)
    description = models.TextField(verbose_name="Описание выполняемых работ", blank=True, null=True)
    email = models.EmailField(verbose_name="Электронная почта", blank=True, null=True)


    def generate_confirmation_token(self):
        self.confirmation_token = str(uuid.uuid4())
        self.save()
        return self.confirmation_token

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.groups.clear()
        if self.role == "superadmin":
            group = Group.objects.get(name="Superadmin")
        elif self.role == "admin":
            group = Group.objects.get(name="Admin")
        elif self.role == "employee":
            group = Group.objects.get(name="Employee")
        else:
            group = Group.objects.get(name="Client")
        self.groups.add(group)

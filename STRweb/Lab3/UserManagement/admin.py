from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


make_inactive.short_description = "Отметить как неактивных"


def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


make_active.short_description = "Отметить как активных"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Личная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "photo",
                    "description",
                )
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
        ("Дополнительные поля", {"fields": ("role", "confirmation_token")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "role",
                    "phone_number",
                    "photo",
                    "description",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "phone_number",
        "role",
        "is_staff",
        "is_active",
        "photo",  # Добавим photo для просмотра в списке пользователей
    )
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email", "phone_number")
    ordering = ("email",)

    # Ваши кастомные действия
    actions = [make_inactive, make_active]

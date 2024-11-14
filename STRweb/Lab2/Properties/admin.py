from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Apartment, House, CommercialProperty, Garage, Photo, ChangeRequest


class PhotoInline(GenericTabularInline):
    model = Photo
    extra = 1


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "street",
        "price",
        "rooms",
        "total_area",
        "year_built",
    )
    search_fields = ("title", "city", "street")
    list_filter = ("city", "rooms", "year_built")
    inlines = [PhotoInline]


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "street",
        "price",
        "bedrooms",
        "plot_area",
        "year_built",
    )
    search_fields = ("title", "city", "street")
    list_filter = ("city", "bedrooms", "year_built")
    inlines = [PhotoInline]


@admin.register(CommercialProperty)
class CommercialPropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "street",
        "price",
        "property_type",
        "floor",
        "total_floors",
    )
    search_fields = ("title", "city", "street")
    list_filter = ("city", "property_type", "year_built")
    inlines = [PhotoInline]


@admin.register(Garage)
class GarageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "street",
        "price",
        "garage_type",
        "space_area",
        "year_built",
    )
    search_fields = ("title", "city", "street")
    list_filter = ("city", "garage_type", "year_built")
    inlines = [PhotoInline]


@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "property_type",
        "property_id",
        "user",
        "change_type",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "change_type", "property_type")
    search_fields = ("user__username", "property_type")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    actions = ["approve_change_requests", "reject_change_requests"]

    def approve_change_requests(self, request, queryset):
        queryset.update(status="approved")
        self.message_user(request, "Выбранные запросы были одобрены.")

    approve_change_requests.short_description = "Одобрить выбранные запросы"

    def reject_change_requests(self, request, queryset):
        queryset.update(status="rejected")
        self.message_user(request, "Выбранные запросы были отклонены.")

    reject_change_requests.short_description = "Отклонить выбранные запросы"

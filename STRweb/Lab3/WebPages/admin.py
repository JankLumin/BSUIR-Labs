from django.contrib import admin
from .models import (
    News,
    CompanyInfo,
    FAQ,
    JobOpening,
    Banner,
    Partner,
    Review,
    PromoCode,
    Contact,
)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["id", "image_tag", "link"]
    readonly_fields = ["image_tag"]

    def image_tag(self, obj):
        from django.utils.html import format_html

        return format_html(
            '<img src="{}" style="width: 45px; height:45px;" />', obj.image.url
        )

    image_tag.short_description = "Image"


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ["name", "logo_tag", "website"]
    readonly_fields = ["logo_tag"]

    def logo_tag(self, obj):
        from django.utils.html import format_html

        if obj.logo:
            return format_html(
                '<img src="{}" style="width: 45px; height:45px;" />', obj.logo.url
            )
        return "-"

    logo_tag.short_description = "Logo"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "rating", "date_posted", "comment"]
    list_filter = ["rating", "date_posted"]
    search_fields = ["user__username", "comment"]


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "active", "discount", "expiration_date"]
    list_filter = ["active", "expiration_date"]
    search_fields = ["code"]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "published_date", "summary"]
    list_filter = ["published_date"]
    search_fields = ["title", "content"]


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ["name", "about", "history", "requisites"]
    readonly_fields = ["logo_image_display"]

    def logo_image_display(self, obj):
        from django.utils.html import format_html

        if obj.logo:
            return format_html('<img src="{}" style="width: 100px;" />', obj.logo.url)
        return "-"

    logo_image_display.short_description = "Logo Preview"


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "answer", "added_date"]
    search_fields = ["question", "answer"]
    list_filter = ["added_date"]


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ["title", "location", "posted_date"]
    list_filter = ["posted_date", "location"]
    search_fields = ["title", "description", "requirements"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "email",
        "phone",
        "job_description",
        "photo_preview",
    ]
    search_fields = ["full_name", "email", "phone"]
    list_filter = ["job_description"]
    readonly_fields = ["photo_preview"]

    def photo_preview(self, obj):
        from django.utils.html import format_html

        if obj.photo_url:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px;" />', obj.photo_url
            )
        return "-"

    photo_preview.short_description = "Фото"

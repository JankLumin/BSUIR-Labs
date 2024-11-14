from rest_framework import serializers
from .models import (
    News,
    CompanyInfo,
    FAQ,
    JobOpening,
    Banner,
    Partner,
    Review,
    PromoCode,
)


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class CompanyInfoSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    certificate_image = serializers.SerializerMethodField()

    class Meta:
        model = CompanyInfo
        fields = "__all__"

    def get_logo(self, obj):
        if obj.logo:
            return self.context["request"].build_absolute_uri(obj.logo.url)
        return None

    def get_certificate_image(self, obj):
        if obj.certificate_image:
            return self.context["request"].build_absolute_uri(obj.certificate_image.url)
        return None


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class JobOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = "__all__"

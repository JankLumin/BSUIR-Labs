from rest_framework import serializers
from .models import Apartment, House, CommercialProperty, Garage, Photo, ChangeRequest


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["image"]


class ApartmentSerializer(serializers.ModelSerializer):
    photos_read = PhotoSerializer(source="photos", many=True, read_only=True)
    photos_write = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Apartment
        fields = [
            "id",
            "city",
            "street",
            "building",
            "building_section",
            "price",
            "ownership",
            "transaction_condition",
            "title",
            "description",
            "contacts",
            "unit_type",
            "rooms",
            "floor",
            "total_floors",
            "renovation",
            "balcony",
            "bathroom",
            "ceiling_height",
            "total_area",
            "living_area",
            "kitchen_area",
            "year_built",
            "photos_read",
            "photos_write",
        ]

    def create(self, validated_data):
        photos_data = validated_data.pop("photos_write", [])
        apartment = Apartment.objects.create(**validated_data)
        for photo_data in photos_data:
            Photo.objects.create(content_object=apartment, image=photo_data)
        return apartment


class HouseSerializer(serializers.ModelSerializer):
    photos_read = PhotoSerializer(source="photos", many=True, read_only=True)
    photos_write = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = House
        fields = [
            "id",
            "city",
            "street",
            "building",
            "building_section",
            "price",
            "ownership",
            "transaction_condition",
            "title",
            "description",
            "contacts",
            "house_type",
            "bedrooms",
            "year_built",
            "wall_material",
            "total_area",
            "living_area",
            "kitchen_area",
            "plot_area",
            "renovation",
            "photos_read",
            "photos_write",
        ]

    def create(self, validated_data):
        photos_data = validated_data.pop("photos_write", [])
        house = House.objects.create(**validated_data)
        for photo_data in photos_data:
            Photo.objects.create(content_object=house, image=photo_data)
        return house


class CommercialPropertySerializer(serializers.ModelSerializer):
    photos_read = PhotoSerializer(source="photos", many=True, read_only=True)
    photos_write = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = CommercialProperty
        fields = [
            "id",
            "city",
            "street",
            "building",
            "building_section",
            "price",
            "ownership",
            "transaction_condition",
            "title",
            "description",
            "contacts",
            "property_type",
            "separate_spaces_range",
            "floor",
            "total_floors",
            "renovation",
            "bathroom",
            "phone_lines",
            "ceiling_height",
            "water_supply",
            "gas_supply",
            "electricity",
            "heating",
            "wall_material",
            "space_area_range",
            "plot_area",
            "building_class",
            "year_built",
            "has_legal_address",
            "photos_read",
            "photos_write",
        ]

    def create(self, validated_data):
        photos_data = validated_data.pop("photos_write", [])
        commercial_property = CommercialProperty.objects.create(**validated_data)
        for photo_data in photos_data:
            Photo.objects.create(content_object=commercial_property, image=photo_data)
        return commercial_property


class GarageSerializer(serializers.ModelSerializer):
    photos_read = PhotoSerializer(source="photos", many=True, read_only=True)
    photos_write = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Garage
        fields = [
            "id",
            "city",
            "street",
            "building",
            "building_section",
            "price",
            "ownership",
            "transaction_condition",
            "title",
            "description",
            "contacts",
            "garage_type",
            "separate_spaces",
            "floor",
            "total_floors",
            "renovation",
            "bathroom",
            "ceiling_height",
            "water_supply",
            "gas_supply",
            "electricity",
            "heating",
            "wall_material",
            "space_area",
            "year_built",
            "photos_read",
            "photos_write",
        ]

    def create(self, validated_data):
        photos_data = validated_data.pop("photos_write", [])
        garage = Garage.objects.create(**validated_data)
        for photo_data in photos_data:
            Photo.objects.create(content_object=garage, image=photo_data)
        return garage


class ChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeRequest
        fields = "__all__"

    def validate(self, data):
        if data["change_type"] in ["create", "update"] and not data.get("data"):
            raise serializers.ValidationError(
                "Поле 'data' обязательно для типов изменений 'create' и 'update'."
            )
        return data

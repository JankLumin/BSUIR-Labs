from django_filters import rest_framework as filters
from .models import Apartment, House, CommercialProperty, Garage


class PropertyFilter(filters.FilterSet):
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")
    street = filters.CharFilter(field_name="street", lookup_expr="icontains")
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        abstract = True
        fields = ["city", "street", "price_min", "price_max"]


class ApartmentFilter(PropertyFilter):
    rooms = filters.RangeFilter()

    class Meta:
        model = Apartment
        fields = ["city", "street", "price_min", "price_max", "rooms"]


class HouseFilter(PropertyFilter):
    bedrooms = filters.RangeFilter()

    class Meta:
        model = House
        fields = ["city", "street", "price_min", "price_max", "bedrooms"]


class CommercialPropertyFilter(PropertyFilter):
    property_type = filters.ChoiceFilter(
        field_name="property_type", lookup_expr="exact"
    )

    class Meta:
        model = CommercialProperty
        fields = ["city", "street", "price_min", "price_max", "property_type"]


class GarageFilter(PropertyFilter):
    garage_type = filters.ChoiceFilter(field_name="garage_type", lookup_expr="exact")

    class Meta:
        model = Garage
        fields = ["city", "street", "price_min", "price_max", "garage_type"]

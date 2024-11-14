from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ApartmentViewSet,
    HouseViewSet,
    CommercialPropertyViewSet,
    GarageViewSet,
    ChangeRequestViewSet,
)

router = DefaultRouter()
router.register(r"apartments", ApartmentViewSet)
router.register(r"houses", HouseViewSet)
router.register(r"commercial_properties", CommercialPropertyViewSet)
router.register(r"garages", GarageViewSet)
router.register(r"changerequests", ChangeRequestViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Apartment, House, CommercialProperty, Garage, ChangeRequest
from .serializers import (
    ApartmentSerializer,
    HouseSerializer,
    CommercialPropertySerializer,
    GarageSerializer,
    ChangeRequestSerializer,
)
from .filters import (
    ApartmentFilter,
    HouseFilter,
    CommercialPropertyFilter,
    GarageFilter,
)
from UserManagement.permissions import IsAdmin, IsClient, IsEmployee, IsSuperAdmin


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApartmentFilter

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsClient]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsEmployee]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        if request.user.role == "employee":
            # Сотрудник создает запрос на добавление нового объекта
            data = request.data
            change_request = ChangeRequest.objects.create(
                user=request.user,
                change_type="create",
                property_type="apartment",
                data=data,
            )
            return Response(
                {"detail": "Ваш запрос был отправлен на рассмотрение."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role == "employee":
            instance = self.get_object()
            data = request.data
            change_request = ChangeRequest.objects.create(
                user=request.user,
                change_type="update",
                property_type="apartment",
                property_id=instance.id,
                data=data,
            )
            return Response(
                {"detail": "Ваш запрос был отправлен на рассмотрение."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role == "employee":
            instance = self.get_object()
            change_request = ChangeRequest.objects.create(
                user=request.user,
                change_type="delete",
                property_type="apartment",
                property_id=instance.id,
            )
            return Response(
                {"detail": "Ваш запрос был отправлен на рассмотрение."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return super().destroy(request, *args, **kwargs)


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = HouseFilter

    def get_permissions(self):
        if self.request.method in ["GET", "HEAD", "OPTIONS"]:
            return [IsClient()]
        elif self.request.user.is_authenticated:
            if self.request.user.role == "employee":
                return [IsEmployee()]
            elif self.request.user.role == "admin":
                return [IsAdmin()]
            elif self.request.user.role == "superadmin":
                return [IsSuperAdmin()]
        return [IsClient()]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsClient]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsEmployee]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        if request.user.role == "employee":
            data = request.data
            change_request = ChangeRequest.objects.create(
                user=request.user,
                change_type="create",
                property_type="apartment",
                data=data,
            )
            return Response(
                {"detail": "Ваш запрос был отправлен на рассмотрение."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role == "employee":
            instance = self.get_object()
            data = request.data
            change_request = ChangeRequest.objects.create(
                user=request.user,
                change_type="update",
                property_type="apartment",
                property_id=instance.id,
                data=data,
            )
            return Response(
                {"detail": "Ваш запрос был отправлен на рассмотрение."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role == "employee":
            instance = self.get_object()
            change_request = ChangeRequest.objects.create(
                user=request.user,
                change_type="delete",
                property_type="apartment",
                property_id=instance.id,
            )
            return Response(
                {"detail": "Ваш запрос был отправлен на рассмотрение."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return super().destroy(request, *args, **kwargs)


class CommercialPropertyViewSet(viewsets.ModelViewSet):
    queryset = CommercialProperty.objects.all()
    serializer_class = CommercialPropertySerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommercialPropertyFilter

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsClient]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsEmployee]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        if request.user.role == "employee":
            data = request.data
            change_request = ChangeRequest.objects.create(
                user=request.user,
                change_type="create",
                property_type="apartment",
                data=data,
            )
            return Response(
                {"detail": "Ваш запрос был отправлен на рассмотрение."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role == "employee":
            instance = self.get_object()
            data = request.data
            change_request = ChangeRequest.objects.create(
                user=request.user,
                change_type="update",
                property_type="apartment",
                property_id=instance.id,
                data=data,
            )
            return Response(
                {"detail": "Ваш запрос был отправлен на рассмотрение."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role == "employee":
            instance = self.get_object()
            change_request = ChangeRequest.objects.create(
                user=request.user,
                change_type="delete",
                property_type="apartment",
                property_id=instance.id,
            )
            return Response(
                {"detail": "Ваш запрос был отправлен на рассмотрение."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return super().destroy(request, *args, **kwargs)


class GarageViewSet(viewsets.ModelViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = GarageFilter

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsClient]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsEmployee]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        if request.user.role == "employee":
            data = request.data
            change_request = ChangeRequest.objects.create(
                user=request.user,
                change_type="create",
                property_type="apartment",
                data=data,
            )
            return Response(
                {"detail": "Ваш запрос был отправлен на рассмотрение."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role == "employee":
            instance = self.get_object()
            data = request.data
            change_request = ChangeRequest.objects.create(
                user=request.user,
                change_type="update",
                property_type="apartment",
                property_id=instance.id,
                data=data,
            )
            return Response(
                {"detail": "Ваш запрос был отправлен на рассмотрение."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role == "employee":
            instance = self.get_object()
            change_request = ChangeRequest.objects.create(
                user=request.user,
                change_type="delete",
                property_type="apartment",
                property_id=instance.id,
            )
            return Response(
                {"detail": "Ваш запрос был отправлен на рассмотрение."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return super().destroy(request, *args, **kwargs)


class ChangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        elif self.action == "create":
            permission_classes = [IsAuthenticated, IsEmployee]
        else:
            permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if (
            request.user.role in ["admin", "superadmin"]
            and instance.status == "pending"
        ):
            return super().update(request, *args, **kwargs)
        return Response(
            {"detail": "У вас нет прав для выполнения этого действия."},
            status=status.HTTP_403_FORBIDDEN,
        )

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if (
            request.user.role in ["admin", "superadmin"]
            and instance.status == "pending"
        ):
            return super().destroy(request, *args, **kwargs)
        return Response(
            {"detail": "У вас нет прав для выполнения этого действия."},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(detail=True, methods=["post"], url_path="approve")
    def approve_request(self, request, pk=None):
        change_request = self.get_object()
        if change_request.status != "pending":
            return Response(
                {"detail": "Запрос уже обработан."}, status=status.HTTP_400_BAD_REQUEST
            )

        if change_request.change_type == "delete":
            self.perform_delete(change_request)
        elif change_request.change_type == "update":
            self.perform_update(change_request)
        elif change_request.change_type == "create":
            self.perform_create_property(change_request)

        change_request.status = "approved"
        change_request.save()
        return Response(
            {"detail": "Запрос был одобрен и изменения выполнены."},
            status=status.HTTP_200_OK,
        )

    def perform_delete(self, change_request):
        """Логика удаления объекта недвижимости"""
        model_class = self.get_model_class(change_request.property_type)
        if model_class:
            model_class.objects.filter(id=change_request.property_id).delete()

    def perform_update(self, change_request):
        """Логика обновления объекта недвижимости"""
        model_class = self.get_model_class(change_request.property_type)
        if model_class:
            instance = model_class.objects.filter(id=change_request.property_id).first()
            if instance:
                for key, value in change_request.data.items():
                    setattr(instance, key, value)
                instance.save()

    def perform_create_property(self, change_request):
        """Логика создания нового объекта недвижимости"""
        model_class = self.get_model_class(change_request.property_type)
        if model_class:
            model_class.objects.create(**change_request.data)

    def get_model_class(self, property_type):
        """Возвращает класс модели на основе типа недвижимости"""
        model_mapping = {
            "Apartment": Apartment,
            "House": House,
            "CommercialProperty": CommercialProperty,
            "Garage": Garage,
        }
        return model_mapping.get(property_type)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject_request(self, request, pk=None):
        change_request = self.get_object()
        if change_request.status != "pending":
            return Response(
                {"detail": "Запрос уже обработан."}, status=status.HTTP_400_BAD_REQUEST
            )

        change_request.status = "rejected"
        change_request.save()
        return Response({"detail": "Запрос был отклонен."}, status=status.HTTP_200_OK)

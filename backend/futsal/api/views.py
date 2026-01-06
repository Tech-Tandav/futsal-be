from rest_framework import viewsets
from backend.futsal.models import Futsal, Booking, TimeSlot
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, permissions
from django.db.models import Prefetch
from backend.futsal.api.serializers import (
    FutsalSerializer,
    FutsalCreateUpdateSerializer,
    TimeSlotSerializer,
    BookingReadSerializer,
    BookingCreateSerializer,
    BookingStatusUpdateSerializer,
)
from backend.futsal.filters import FutsalFilter, TimeSlotFilter, BookingFilter
from backend.futsal.throttles import BookingRateThrottle


class FutsalViewSet(viewsets.ModelViewSet):
    queryset = (
        Futsal.objects
        .filter(is_active=True)
        .prefetch_related("futsal_image")
    )
    filterset_class = FutsalFilter
    search_fields = ["name", "city"]
    ordering_fields = ["price_per_hour", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return FutsalCreateUpdateSerializer
        return FutsalSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TimeSlotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        TimeSlot.objects
        .select_related("futsal")
        .order_by("day_of_week", "start_time")
    )
    serializer_class = TimeSlotSerializer
    filterset_class = TimeSlotFilter
    ordering_fields = ["day_of_week", "start_time"]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = (
        Booking.objects
        .select_related("time_slot", "time_slot__futsal")
    )
    filterset_class = BookingFilter
    search_fields = ["customer_name", "customer_phone", "customer_email"]
    ordering_fields = ["created_at", "date"]
    ordering = ["-created_at"]
    throttle_classes = [BookingRateThrottle]  
    
    
    def get_serializer_class(self):
        if self.action == "create":
            return BookingCreateSerializer
        if self.action in ["update", "partial_update"]:
            return BookingStatusUpdateSerializer
        return BookingReadSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

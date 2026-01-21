from rest_framework import viewsets
from backend.futsal.models import Futsal, Booking, TimeSlot
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import APIException
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, permissions, generics
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
    permission_classes = [AllowAny]
    
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
    permission_classes = [AllowAny]
    pagination_class = None
   


class BookingListCreateAPIView(generics.ListCreateAPIView):
    filterset_class = BookingFilter
    search_fields = ["customer_name", "customer_phone", "customer_email"]
    ordering_fields = ["created_at", "date"]
    ordering = ["-created_at"]
    throttle_classes = [BookingRateThrottle]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookingCreateSerializer
        return BookingReadSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        qs = Booking.objects.select_related(
            "time_slot",
            "time_slot__futsal"
        )

        if user.is_staff:
            return qs.filter(time_slot__futsal__owner=user)

        return qs.filter(user=user)

class BookingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  Booking.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return BookingStatusUpdateSerializer
        return BookingReadSerializer

    # def get_queryset(self):
    #     user = self.request.user

    #     qs = Booking.objects.select_related(
    #         "time_slot",
    #         "time_slot__futsal"
    #     )

    #     if user.is_staff:
    #         return qs.filter(time_slot__futsal__owner=user)

    #     return qs.filter(user=user)

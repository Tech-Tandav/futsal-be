from rest_framework import viewsets
from backend.futsal.models import Futsal, Booking, TimeSlot
from .serializers import FutsalSerializer, BookingSerializer, TimeSlotSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class FutsalViewSet(viewsets.ModelViewSet):
    queryset = Futsal.objects.filter(is_active=True)
    serializer_class = FutsalSerializer
    permission_classes = [AllowAny]


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.filter(is_active=True)
    serializer_class = TimeSlotSerializer
    permission_classes = [AllowAny]
    

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



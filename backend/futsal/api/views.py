from rest_framework import viewsets
from backend.futsal.models import Futsal, Booking, TimeSlot
from .serializers import FutsalSerializer, BookingSerializer, TimeSlotSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class FutsalViewSet(viewsets.ModelViewSet):
    queryset = Futsal.objects.filter(is_archived=False)
    serializer_class = FutsalSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name", "city", "address"]  

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.filter(is_archived=False)
    serializer_class = TimeSlotSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["futsal"]
    

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.filter(is_archived=False)
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     return Booking.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)



from rest_framework import serializers
from backend.futsal.models import Futsal, FutsalImage, TimeSlot, Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        

class TimeSlotSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source="get_day_of_week_display", read_only=True)

    class Meta:
        model = TimeSlot
        exclude = ["created_at", "updated_at"]


class FutsalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutsalImage
        exclude = ["created_at", "updated_at"]


class FutsalSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True, read_only=True)
    futsal_image = FutsalImageSerializer(many=True, read_only=True)
    class Meta:
        model = Futsal
        fields = "__all__"



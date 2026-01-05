from rest_framework import serializers
from backend.futsal.models import Futsal, FutsalImage, TimeSlot, Booking
    

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


class BookingSerializer(serializers.ModelSerializer):
    time_slot = TimeSlotSerializer(read_only=True)
    time_slot_id = serializers.PrimaryKeyRelatedField(
        queryset=TimeSlot.objects.all(), source='time_slot', write_only=True
    )
    futsal_name = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = "__all__"
        
    def get_futsal_name(self,obj):
        return obj.time_slot.futsal.name
from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from backend.futsal.models import Futsal, FutsalImage, TimeSlot, Booking
    
    
class FutsalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutsalImage
        fields = ["id", "image"]



class FutsalSerializer(serializers.ModelSerializer):
    images = FutsalImageSerializer(source="futsal_image", many=True, read_only=True)
    # distance = serializers.SerializerMethodField()
    class Meta:
        model = Futsal
        fields = [
            "id",
            "name",
            "address",
            "city",
            "latitude",
            "longitude",
            "price_per_hour",
            "amenities",
            "is_active",
            "image",
            "images",
            # "distance",
            "created_at",
        ]
    # def get_distance(self,obj):
    #     print(self.context.get("request").query_params)
    #     return 1

class FutsalCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Futsal
        fields = [
            "name",
            "address",
            "city",
            "latitude",
            "longitude",
            "price_per_hour",
            "amenities",
            "image",
            "is_active",
        ]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)



class TimeSlotSerializer(serializers.ModelSerializer):
    futsal_name = serializers.CharField(source="futsal.name", read_only=True)
    day_name = serializers.CharField(source="get_day_of_week_display", read_only=True)
    booking = serializers.SerializerMethodField()
    class Meta:
        model = TimeSlot
        fields = [
            "id",
            "futsal",
            "futsal_name",
            "day_of_week",
            "start_time",
            "end_time",
            "status",
            "day_name",
            "booking"
        ]
        
    def get_booking(self, obj):
        if self.context["request"].user.is_staff:
            return obj.booking_set.values("id", "customer_name", "customer_phone", "status" ,"date").order_by("date")
        return []



class BookingReadSerializer(serializers.ModelSerializer):
    futsal_name = serializers.CharField(source="time_slot.futsal.name", read_only=True)
    start_time = serializers.TimeField(source="time_slot.start_time", read_only=True)
    end_time = serializers.TimeField(source="time_slot.end_time", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "futsal_name",
            "date",
            "start_time",
            "end_time",
            "customer_name",
            "customer_phone",
            "customer_email",
            "status",
            "created_at",
        ]



class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "time_slot",
            "date",
            "customer_name",
            "customer_phone",
            "customer_email",
        ]

    def validate(self, attrs):
        time_slot = attrs["time_slot"]
        date = attrs.get("date")
        if not date:
            raise serializers.ValidationError({"date": "Booking date is required."})

        if date < timezone.now().date():
            raise serializers.ValidationError({"date": "Cannot book past dates."})

        exists = Booking.objects.filter(
            time_slot=time_slot,
            date=date,
            status="confirmed",
        ).exists()

        if exists:
            raise serializers.ValidationError(
                "This time slot is already confirmed for the selected date."
            )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get("request")

        booking = Booking.objects.create(
            user=request.user if request and request.user.is_authenticated else None,
            status="pending",
            **validated_data,
        )

        time_slot = booking.time_slot
        time_slot.status = "in_queue"
        time_slot.save(update_fields=["status"])

        return booking


class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["status"]

    def validate_status(self, value):
        if value not in ["confirmed", "rejected"]:
            raise serializers.ValidationError("Invalid status update.")
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        status = validated_data["status"]

        instance.status = status
        instance.save(update_fields=["status"])

        time_slot = instance.time_slot

        if status == "confirmed":
            time_slot.status = "booked"

            Booking.objects.filter(
                time_slot=time_slot,
                date=instance.date,
            ).exclude(id=instance.id).update(status="rejected")

        elif status == "rejected":
            if not Booking.objects.filter(
                time_slot=time_slot,
                date=instance.date,
                status="confirmed",
            ).exists():
                time_slot.status = "available"

        time_slot.save(update_fields=["status"])
        return instance

from datetime import datetime
from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from django.forms.models import model_to_dict
from backend.futsal.models import Futsal, FutsalImage, TimeSlot, Booking
from backend.core.utils import get_day_key
    
    
class FutsalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutsalImage
        fields = ["id", "image"]



class FutsalSerializer(serializers.ModelSerializer):
    images = FutsalImageSerializer(source="futsal_image", many=True, read_only=True)
    # distance = serializers.SerializerMethodField()
    price_per_hour = serializers.SerializerMethodField()
    class Meta:
        model = Futsal
        fields = [
            "id",
            "name",
            "address",
            "city",
            "phone",
            "latitude",
            "longitude",
            "amenities",
            "is_active",
            "image",
            "images",
            "created_at",
            "map_source",
            "price_per_hour",
            # "distance"
        ]
    # def get_distance(self,obj):
    #     print(self.context.get("request").query_params)
    #     return 1
    def get_price_per_hour(self,obj):
        date_str = self.context.get("date")
        time_slot = self.context.get("time_slot")
        if date_str:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            time_slot_obj = TimeSlot.objects.get(id=time_slot)
            day_key = get_day_key(dt)
            priceing_obj = obj.prices.filter(
                day=day_key,
                start_time__lte=time_slot_obj.start_time,
                end_time__gt=time_slot_obj.end_time
            ).first()
        else:
            now = timezone.localtime()
            day_key = get_day_key(now)
            priceing_obj = obj.prices.filter(
                day=day_key,
                start_time__lte=now.time(),
                end_time__gt=now.time()
            ).first()
        return model_to_dict(priceing_obj)["price_per_hour"] if priceing_obj else None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field in ["map_source"]:
            if representation.get(field) == "":
                representation[field] = None
        return representation

class FutsalCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Futsal
        fields = [
            "name",
            "address",
            "city",
            "latitude",
            "longitude",
            "amenities",
            "image",
            "phone",
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
        today = timezone.now().date()
        user_obj = self.context["request"].user
        if  user_obj.is_staff:
            return obj.booking_set.filter(date__gte=today, time_slot__futsal__owner=user_obj).values("id", "customer_name", "customer_phone", "status", "date" ,"created_at").order_by("created_at")
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
            # print(Booking.objects.filter(
            #     time_slot=time_slot,
            #     date=instance.date,
            # ).exclude(Q(id=instance.id) | Q(status="rejected")).values("id", "status"))
            if not Booking.objects.filter(
                time_slot=time_slot,
                date=instance.date,
                ).exclude(Q(id=instance.id) | Q(status="rejected")).exists():
                time_slot.status = "available"

        time_slot.save(update_fields=["status"])
        return instance

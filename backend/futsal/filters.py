import django_filters
from backend.futsal.models import Futsal, FutsalImage, TimeSlot, Booking


class FutsalFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name="price_per_hour", lookup_expr="gte"
    )
    max_price = django_filters.NumberFilter(
        field_name="price_per_hour", lookup_expr="lte"
    )

    class Meta:
        model = Futsal
        fields = ["city", "is_active"]


class TimeSlotFilter(django_filters.FilterSet):
    class Meta:
        model = TimeSlot
        fields = ["futsal", "day_of_week", "status"]


class BookingFilter(django_filters.FilterSet):
    date = django_filters.DateFilter()
    from_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    to_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Booking
        fields = ["status", "time_slot"]

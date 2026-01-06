# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from backend.futsal.models import Futsal, FutsalImage, TimeSlot, Booking
from backend.core.admin import BaseModelAdmin


class FutsalImageInline(admin.StackedInline):
    model = FutsalImage
    extra = 0
    # show_change_link = True
    fieldsets = (
        (None, {
            "fields": ("image",)
        }),
    )


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 0
    # show_change_link = True
    fieldsets = (
        (None, {
            "fields": ("day_of_week", "start_time", "end_time", 'is_archived')
        }),
    )
    
    
@admin.register(Futsal)
class FutsalAdmin(BaseModelAdmin):
    list_display = (
        "name",
        "price_per_hour",
        "owner",
        "image_preview",
        "created_at",
        "is_active",
    )
    list_filter = (
        "created_at",
        'city'
    )
    search_fields = (
        "name",
        "city"
    )
    ordering = ("-created_at",)

    readonly_fields = ("image_preview", "created_at", 'updated_at')

    fieldsets = (
        ("Basic Info", {
            "fields": (
                "name",
                "city",
                "address",
                "price_per_hour",
                "owner",
            )
        }),
        ("Location", {
            "fields": (
                "latitude",
                "longitude",
            )
        }),
        ("Facilities", {
            "fields": (
                "amenities",
            )
        }),
        ("Media", {
            "fields": (
                "image",
                "image_preview",
            )
        }),
        ("Other", {
            "fields": (
                "is_active",
                "is_archived",
                "created_at",
                "updated_at"
            )
        }),
    )
    inlines = [FutsalImageInline, TimeSlotInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="120" style="border-radius:6px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # Columns shown in admin list view
    list_display = (
        "id",
        "customer_name",
        "customer_phone",
        "customer_email",
        "time_slot",
        "date",
        "status",
        "created_at",
    )

    # Filters on right sidebar
    list_filter = (
        "status",
        "date",
        "created_at",
    )

    # Search bar fields
    search_fields = (
        "customer_name",
        "customer_phone",
        "customer_email",
        "time_slot__futsal__name",
    )

    # Ordering (uses your Meta ordering as fallback)
    ordering = ("-created_at",)

    # Use dropdowns for FK fields (faster than raw_id_fields for small data)
    autocomplete_fields = ( "user", )

    # Fields editable directly in list view
    list_editable = ("status", "date")

    # Read-only fields
    readonly_fields = ("created_at", "updated_at")

    # Group fields nicely in detail view
    fieldsets = (
        ("Customer Information", {
            "fields": (
                "customer_name",
                "customer_phone",
                "customer_email",
                "user",
            )
        }),
        ("Booking Details", {
            "fields": (
                "time_slot",
                "date",
                "status",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    # Admin actions
    actions = ["mark_confirmed", "mark_rejected"]

    def mark_confirmed(self, request, queryset):
        queryset.update(status="confirmed")
    mark_confirmed.short_description = "Mark selected bookings as Confirmed"

    def mark_rejected(self, request, queryset):
        queryset.update(status="rejected")
    mark_rejected.short_description = "Mark selected bookings as Rejected"
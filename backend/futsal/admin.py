# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from backend.futsal.models import Futsal, FutsalImage, TimeSlot
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
            "fields": ("day_of_week", "start_time", "end_time")
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

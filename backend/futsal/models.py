from django.conf import settings
from django.db import models
from backend.core.models import BaseModel
from django.db.models import Q


class Futsal(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    amenities = models.JSONField(default=list, blank=True,null=True)  
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    image = models.FileField(upload_to="futsal/",blank=True,null=True)
    map_source = models.TextField(blank=True,null=True)
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class FutsalPrice(BaseModel):
    DAY_CHOICES = [
        ('weekday', 'Weekdays (Sun–Fri)'),
        ('sat', 'Saturday'),
    ]

    futsal = models.ForeignKey(
        Futsal,
        on_delete=models.CASCADE,
        related_name='prices'
    )

    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.futsal.name}=>{self.day}:{self.start_time}-{self.end_time}={self.price_per_hour}"


class FutsalPricingConfig(BaseModel):
    futsal = models.OneToOneField(
        Futsal,
        on_delete=models.CASCADE,
        related_name="pricing_config"
    )

    weekday_open = models.TimeField()
    weekday_close = models.TimeField()

    off_start = models.TimeField()
    off_end = models.TimeField()

    peak_price = models.DecimalField(max_digits=8, decimal_places=2)
    off_price = models.DecimalField(max_digits=8, decimal_places=2)
    saturday_price = models.DecimalField(max_digits=8, decimal_places=2)



class FutsalImage(BaseModel):
    futsal = models.ForeignKey(Futsal, on_delete=models.CASCADE, related_name="futsal_image")
    image = models.FileField(upload_to="futsal/other/",blank=True,null=True)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.futsal.name


class TimeSlot(BaseModel):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("booked", "Booked"),
        ("in_queue", "In Queue"),
    ]

    futsal = models.ForeignKey(Futsal, on_delete=models.CASCADE, related_name="time_slots")
    day_of_week = models.IntegerField()  
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="available")
    
    class Meta:
         ordering = ["day_of_week", "start_time", "end_time"]

        
    def __str__(self):
        return f"{self.futsal.name} - {self.day_of_week} {self.start_time}-{self.end_time}"


class Booking(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)  
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    request_mail_status = models.BooleanField(default=False)
    decision_mail_status = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["time_slot", "date"],
                condition=Q(status="confirmed"),
                name="unique_confirmed_booking_per_day"
            )
        ]
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
    def __str__(self):
        return f"{self.customer_name} - {self.time_slot.futsal.name} - {self.status}"
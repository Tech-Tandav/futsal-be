from rest_framework.throttling import UserRateThrottle

class BookingRateThrottle(UserRateThrottle):
    scope = "booking"

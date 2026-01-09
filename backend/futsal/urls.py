from rest_framework.routers import DefaultRouter
from backend.futsal.api.views import FutsalViewSet, BookingListCreateAPIView, TimeSlotViewSet, BookingRetrieveUpdateDestroyAPIView
from django.urls import path
router = DefaultRouter()
router.register("futsals", FutsalViewSet, basename="futsal")
router.register("time-slots", TimeSlotViewSet, basename="time-slot")
# router.register("booking", BookingViewSet, basename="booking")

urlpatterns = router.urls



urlpatterns = [
    path("bookings/", BookingListCreateAPIView.as_view()),
    path("bookings/<int:pk>/", BookingRetrieveUpdateDestroyAPIView.as_view()),
]
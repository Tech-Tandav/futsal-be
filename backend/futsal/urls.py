from rest_framework.routers import DefaultRouter
from backend.futsal.api.views import FutsalViewSet, BookingViewSet, TimeSlotViewSet

router = DefaultRouter()
router.register("futsals", FutsalViewSet, basename="futsal")
router.register("time-slot", TimeSlotViewSet, basename="time-slot")
router.register("booking", BookingViewSet, basename="booking")

urlpatterns = router.urls

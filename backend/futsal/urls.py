from rest_framework.routers import DefaultRouter
from backend.futsal.api.views import FutsalViewSet, BookingViewSet

router = DefaultRouter()
router.register("futsals", FutsalViewSet, basename="futsal")
router.register("time-slot", FutsalViewSet, basename="futsal")
router.register("bookings", BookingViewSet, basename="booking")

urlpatterns = router.urls

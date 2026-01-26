from rest_framework.routers import DefaultRouter
from backend.futsal.api.views import FutsalViewSet, BookingCreateAPIView, BookingListAPIView,TimeSlotViewSet, BookingRetrieveUpdateDestroyAPIView
from django.urls import path
router = DefaultRouter()
router.register("futsals", FutsalViewSet, basename="futsal")
router.register("time-slots", TimeSlotViewSet, basename="time-slot")
# router.register("booking", BookingViewSet, basename="booking")





urlpatterns = [
    path("booking/<uuid:pk>/", BookingRetrieveUpdateDestroyAPIView.as_view()),
    path("booking/create/", BookingCreateAPIView.as_view()),
    path("booking/", BookingListAPIView.as_view()),
    
]

urlpatterns += router.urls
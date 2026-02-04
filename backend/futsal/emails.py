from backend.core.mail import BaseEmailMessage  

class BookingNotificationForOnwerEmail(BaseEmailMessage):
    template_name = "emails/booking_notification_for_owner.html"
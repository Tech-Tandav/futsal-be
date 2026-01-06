from datetime import time
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from backend.futsal.models import Futsal, TimeSlot, Booking


@receiver(post_save, sender=Futsal, weak=False)
def create_time_slot(sender, instance, created, **kwargs):
    try:
        if created:
            TIME_SLOTS = [
                "06:00","07:00","08:00","09:00","10:00","11:00",
                "12:00","13:00","14:00","15:00","16:00","17:00",
                "18:00","19:00","20:00","21:00","22:00","23:00"
            ]            
            for day in range(7):
                print(day)
                for i in range(len(TIME_SLOTS) - 1):
                    start = time.fromisoformat(TIME_SLOTS[i])
                    end = time.fromisoformat(TIME_SLOTS[i + 1])
                    TimeSlot.objects.create(
                        futsal=instance,
                        day_of_week=day,
                        start_time=start,
                        end_time=end
                    )
    except Exception as e:
        print(f"Error in {instance}: {str(e)}")



@receiver(post_save, sender=Booking)
def create_time_slot(sender, instance, created, **kwargs):
    if created:
        instance.time_slot.status = "in_queue"
        instance.time_slot.save()
        return
    if instance.status == "confirmed":
        instance.time_slot.status = "booked"
        instance.time_slot.save()
        Booking.objects.filter(
            time_slot=instance.time_slot
        ).exclude(id=instance.id).update(status="rejected")
        
            
    
        
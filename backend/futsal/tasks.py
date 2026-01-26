from celery import shared_task
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from backend.futsal.models import Futsal, TimeSlot, Booking

def time_slot_12am():
    task_name = 'Time Slot '
    if not PeriodicTask.objects.filter(name=task_name).exists():
        schedule, _ = CrontabSchedule.objects.get_or_create(
            hour=0,  
            minute=0,
            timezone='Asia/Kathmandu'
        )

        PeriodicTask.objects.create(
            crontab=schedule,  
            name=task_name,  
            task='backend.futsal.tasks.time_slot',
            enabled=True, 
        )
        print(f"Scheduled task '{task_name}' for 12 AM Nepal time.")
    else:
        print(f"Task '{task_name}' already exists.")





@shared_task
def time_slot():
    python_day = timezone.localdate().weekday()
    django_day = (python_day + 1) % 7
    TimeSlot.objects.filter(day_of_week=django_day).update(status='available')
    # cron_started("mark_students_absent", today, day_of_week)
    
    # cron_ended("mark_students_absent")


@shared_task
def send_booking_mail(instance_id):
    instance = Booking.objects.get(id=instance_id)
    link = f"{settings.FE_URL}new-booking/{instance.id}"
    send_mail(
        subject=f'Booking for {instance.time_slot.futsal.name}',
        message=f'''Your booking from {instance.time_slot.start_time}-{instance.time_slot.end_time} is {instance.status}''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.customer_email],
        fail_silently=False,
    )
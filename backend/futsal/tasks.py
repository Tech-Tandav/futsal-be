from celery import shared_task
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from backend.futsal.models import Futsal, TimeSlot, Booking
from backend.futsal.emails import BookingNotificationForOnwerEmail


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


@shared_task
def send_booking_mail_to_customer(instance_id):
    instance = Booking.objects.get(id=instance_id)
    time_slot_obj = instance.time_slot
    futsal_obj = time_slot_obj.futsal
    send_mail(
        subject=f'Booking for {futsal_obj.name}',
        message=f'''Booking for {time_slot_obj.start_time}-{time_slot_obj.end_time} is {instance.status}''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.customer_email],
        fail_silently=False,
    )
    if instance.status == "pending":
        Booking.objects.filter(id=instance.id).update(request_mail_status=True)
    elif instance.status == "confirmed" or instance.status == "rejected":
        Booking.objects.filter(id=instance.id).update(decision_mail_status=True)
    
    
@shared_task
def send_booking_mail_to_owner(instance_id):
    instance = Booking.objects.get(id=instance_id)
    time_slot_obj = instance.time_slot
    futsal_obj = time_slot_obj.futsal
    link = f"{settings.FE_URL}owner/?futsal_id={futsal_obj.id}&timeSlot_id={time_slot_obj.id}&date={instance.date}"
    email = BookingNotificationForOnwerEmail({"link":link}, f"Booking for {time_slot_obj.start_time}-{time_slot_obj.end_time} is {instance.status}")
    email.send(to=[futsal_obj.owner.email])
    
    
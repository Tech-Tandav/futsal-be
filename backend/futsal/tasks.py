from celery import shared_task
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from backend.futsal.models import Futsal, TimeSlot, Booking
from django.utils import timezone


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


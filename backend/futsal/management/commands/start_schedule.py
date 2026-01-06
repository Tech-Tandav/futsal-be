from django.core.management.base import BaseCommand

from backend.futsal.tasks import time_slot_12am


class Command(BaseCommand):
    help = "Used to start periodic task"
    requires_migrations_checks = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        time_slot_12am()

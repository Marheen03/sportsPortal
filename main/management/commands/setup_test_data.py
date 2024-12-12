import random

from django.db import transaction
from django.core.management.base import BaseCommand

from main.models import *
from main.factory import *

NUM_TEAMS = 25
NUM_COMPETITIONS = 4
NUM_MATCHES = 20

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")

        models = [Team, Competition, Match]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        for _ in range(NUM_TEAMS):
            TeamFactory()

        for _ in range(NUM_COMPETITIONS):
            CompetitionFactory()
        
        for _ in range(NUM_MATCHES):
            MatchFactory()
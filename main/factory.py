## factories.py
import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
import random
from main.models import *

## Defining a factory
class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    team_name = factory.Faker("first_name")
    team_stadium = factory.Faker("sentence", nb_words=3)
    team_country = factory.Faker("country")


class CompetitionFactory(DjangoModelFactory):
    class Meta:
        model = Competition

    competition_name = factory.Faker("last_name")
    competition_country = factory.Faker("country")
    
    @factory.post_generation
    def competition_teams(self, create, extracted, **kwargs):
        if extracted:
            # If teams were passed in, assign them to the competition
            for team in extracted:
                self.competition_teams.add(team)
        else:
            # If no teams were passed in, create some default teams and associate them
            teams = TeamFactory.create_batch(2)  # Create 2 teams
            for team in teams:
                self.competition_teams.add(team)


class MatchFactory(DjangoModelFactory):
    class Meta:
        model = Match

    match_date = factory.Faker('date_time_this_year', tzinfo=timezone.get_current_timezone())
    match_stadium = factory.Faker("sentence", nb_words=3)
    match_competition = factory.Iterator(Competition.objects.all())

    @factory.lazy_attribute
    def match_team1(self):
        # select a random team from Team model
        return random.choice(Team.objects.all())
    
    @factory.lazy_attribute
    def match_team2(self):
        team1 = self.match_team1
        # pick a team different from match_team1
        team2 = random.choice(Team.objects.exclude(id=team1.id))
        return team2
    
    match_score1 = factory.Faker('random_int', min=0, max=4)
    match_score2 = factory.Faker('random_int', min=0, max=4)

from django.db import models

# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=50)
    team_stadium = models.TextField()
    team_country = models.CharField(max_length=30)

    def __str__(self):
        return '{}, {}'.format(self.team_name, self.team_country)
    

class Competition(models.Model):
    competition_name = models.CharField(max_length=50)
    competition_country = models.CharField(max_length=30)
    competition_teams = models.ManyToManyField(Team)

    def __str__(self):
        return self.competition_name


class Match(models.Model):
    match_date = models.DateTimeField('Datum utakmice')
    match_stadium = models.TextField()

    match_competition = models.ForeignKey(Competition, on_delete=models.CASCADE, blank=True, null=True)
    match_team1 = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name='team1')
    match_team2 = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name='team2')

    match_score1 = models.IntegerField()
    match_score2 = models.IntegerField()

    def __str__(self):
        return '{}  {} - {}  {}'.format(self.match_team1, self.match_score1, self.match_score2, self.match_team2)
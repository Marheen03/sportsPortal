from django.urls import include, path
from . import views
from main.views import *

urlpatterns = [
    path('', LatestMatches.as_view(), name='index'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/teams/', teamList.as_view(), name='teamsAPI'),
    path('api/teams/<int:pk>/', teamDetail.as_view(), name='teamDetailAPI'),
    
    path('adminDashboard/', UsersList.as_view(), name='usersList'),
    path('adminDashboard/createUser', createUser, name='createUser'),
    path('adminDashboard/editUser/<userID>', editUser, name='editUser'),
    path('adminDashboard/deleteUser/<userID>', deleteUser, name='deleteUser'),

    path('matches/', AllMatches, name='allMatches'),
    path('matches/create', createMatch, name='createMatch'),
    path('matches/<pk>', MatchDetailed.as_view(), name='matchDetails'),
    path('matches/edit/<matchID>', editMatch, name='editMatch'),
    path('matches/delete/<matchID>', deleteMatch, name='deleteMatch'),

    path('teams/', AllTeams.as_view(), name='allTeams'),
    path('teams/create', createTeam, name='createTeam'),
    path('teams/<pk>', TeamDetailed, name='teamDetails'),
    path('teams/edit/<teamID>', editTeam, name='editTeam'),
    path('teams/delete/<teamID>', deleteTeam, name='deleteTeam'),

    path('competitions/', AllCompetitions.as_view(), name='allCompetitions'),
    path('competitions/create', createCompetition, name='createCompetition'),
    path('competitions/<pk>', CompetitionDetailed.as_view(), name='competitionDetails'),
    path('competitions/edit/<competitionID>', editCompetition, name='editCompetition'),
    path('competitions/delete/<competitionID>', deleteCompetition, name='deleteCompetition'),
]
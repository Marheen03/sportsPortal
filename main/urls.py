from django.urls import path
from . import views
from main.views import *

urlpatterns = [
    path('', LatestMatches.as_view(), name='index'),
    
    path('adminDashboard/', UsersList.as_view(), name='usersList'),
    path('adminDashboard/createUser', views.createUser, name='createUser'),
    path('adminDashboard/editUser/<userID>', views.editUser, name='editUser'),
    path('adminDashboard/deleteUser/<userID>', views.deleteUser, name='deleteUser'),

    path('matches/', views.AllMatches, name='allMatches'),
    path('matches/create', views.createMatch, name='createMatch'),
    path('matches/<pk>', MatchDetailed.as_view(), name='matchDetails'),
    path('matches/edit/<matchID>', views.editMatch, name='editMatch'),
    path('matches/delete/<matchID>', views.deleteMatch, name='deleteMatch'),

    path('teams/', AllTeams.as_view(), name='allTeams'),
    path('teams/create', views.createTeam, name='createTeam'),
    path('teams/<pk>', views.TeamDetailed, name='teamDetails'),
    path('teams/edit/<teamID>', views.editTeam, name='editTeam'),
    path('teams/delete/<teamID>', views.deleteTeam, name='deleteTeam'),

    path('competitions/', AllCompetitions.as_view(), name='allCompetitions'),
    path('competitions/create', views.createCompetition, name='createCompetition'),
    path('competitions/<pk>', CompetitionDetailed.as_view(), name='competitionDetails'),
    path('competitions/edit/<competitionID>', views.editCompetition, name='editCompetition'),
    path('competitions/delete/<competitionID>', views.deleteCompetition, name='deleteCompetition'),
]
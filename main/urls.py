from django.urls import path
from . import views
from main.views import UsersList, LatestMatches

urlpatterns = [
    path('', LatestMatches.as_view(), name='index'),
    
    path('adminDashboard/', UsersList.as_view(), name='usersList'),
    path('adminDashboard/createUser', views.createUser, name='createUser'),
    path('adminDashboard/editUser/<userID>', views.editUser, name='editUser'),
    path('adminDashboard/deleteUser/<userID>', views.deleteUser, name='deleteUser'),
]
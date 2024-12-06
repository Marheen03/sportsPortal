from django.urls import path
from . import views
from main.views import UsersList

urlpatterns = [
    path('', views.index, name='index'),
    path('adminDashboard/', UsersList.as_view(), name='usersList'),
    path('adminDashboard/createUser', views.createUser, name='createUser'),
]
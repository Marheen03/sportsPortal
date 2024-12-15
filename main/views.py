from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from itertools import groupby
from django.db.models import Q
from . import forms
from main.models import *

def is_user_admin(user):
    admin_group = Group.objects.get(name="Administrator") 
    return admin_group.user_set.filter(username=user).exists()


class LatestMatches(LoginRequiredMixin, ListView):
    template_name = 'main/index.html'

    def get_queryset(self):
        return Match.objects.order_by('-match_date')[:7]


class UsersList(UserPassesTestMixin, ListView):
    template_name = 'admin/users_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name="Administrator").exists()

    def get_queryset(self):
        return User.objects.all()


@user_passes_test(is_user_admin)
def createUser(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.UserFormCreate(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user_name = form.cleaned_data['username']

            # create new user
            new_user = User.objects.create_user(
                username=user_name,
                password=form.cleaned_data['password']
            )
                    
            user_type = form.cleaned_data['vrsta_korisnika']
            if (user_type == 'Administrator'):
                new_user.is_superuser = True
                new_user.is_staff = True
                new_user.save()
            
            group = Group.objects.get(name=user_type)
            new_user.groups.add(group)

            # add a success message
            messages.success(request, 'Korisnik "{}" je uspješno kreiran!'.format(user_name))
            return HttpResponseRedirect("/adminDashboard")
    else:
        form = forms.UserFormCreate()
    
    return render(request, 'admin/user_form.html', {'form': form, 'form_action': 'create'})


@user_passes_test(is_user_admin)
def editUser(request, userID):
    user = User.objects.get(id=userID)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.UserFormEdit(request.POST, instance=user)

        if form.is_valid():
            user_name = form.cleaned_data['username']
            form.save()

            # add a success message
            messages.success(request, 'Korisnik "{}" je uspješno ažuriran!'.format(user_name))
            return HttpResponseRedirect("/adminDashboard")
    else:
        # populate the form with the chosen user's data
        form = forms.UserFormEdit(instance=user)
    
    return render(request, 'admin/user_form.html', {'form': form, 'form_action': 'edit', 'userID': user.id})


@user_passes_test(is_user_admin)
def deleteUser(request, userID):
    user = User.objects.get(id=userID)
    try:
        user.delete()
        messages.success(request, 'Korisnik "{}" je uspješno obrisan!'.format(user.username))
        return redirect('usersList')
    except User.DoesNotExist:
        return redirect('usersList')


class MatchDetailed(LoginRequiredMixin, DetailView):
    model = Match
    template_name = 'main/matchDetail.html'


@login_required
def AllMatches(request):
    matches = Match.objects.order_by('match_competition', '-match_date')
    grouped_matches = {
        competition: list(matches) 
        for competition, matches in groupby(matches, key=lambda x: x.match_competition)
    }
    return render(request, 'main/matches.html', {'grouped_matches': grouped_matches})


class AllTeams(LoginRequiredMixin, ListView):
    template_name = 'main/teams.html'

    def get_queryset(self):
        return Team.objects.order_by('team_name')


@login_required
def TeamDetailed(request, pk):
    context = {}
    context["object"] = Team.objects.get(id = pk)

    matches = Match.objects.filter(Q(match_team1__id = pk) | Q(match_team2__id = pk)).order_by('-match_date')
    context["grouped_matches"] = {
        competition: list(matches) 
        for competition, matches in groupby(matches, key=lambda x: x.match_competition)
    }
         
    return render(request, "main/teamDetail.html", context)


class AllCompetitions(LoginRequiredMixin, ListView):
    template_name = 'main/competitions.html'

    def get_queryset(self):
        return Competition.objects.order_by('competition_name')


class CompetitionDetailed(LoginRequiredMixin, DetailView):
    model = Competition
    template_name = 'main/competitionDetail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CompetitionDetailed, self).get_context_data(*args, **kwargs)
        context['matches_list'] = Match.objects.filter(match_competition__id = self.kwargs['pk']).order_by('-match_date')
        context['competition_teams'] = self.object.competition_teams.all()
        return context